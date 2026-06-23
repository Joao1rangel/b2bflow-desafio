"""
Desafio b2bflow - Estagio em Desenvolvimento Python
---------------------------------------------------
Le contatos cadastrados no Supabase e envia, via Z-API,
a mensagem: "Ola, <nome_contato> tudo bem com voce?"

Autor: Joao Pedro Salama Rangel (JPSR)
"""

import os
import logging
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

# ---------------------------------------------------------------------------
# Configuracao de logs (boa pratica: rastrear o que acontece em cada etapa)
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("b2bflow")

# ---------------------------------------------------------------------------
# Carrega as variaveis de ambiente do arquivo .env
# ---------------------------------------------------------------------------
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")

# Nome da tabela e limite de envios
TABELA_CONTATOS = "contatos"
LIMITE_ENVIOS = 3


def validar_ambiente() -> bool:
    """Garante que todas as variaveis necessarias foram carregadas."""
    obrigatorias = {
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_KEY": SUPABASE_KEY,
        "ZAPI_INSTANCE_ID": ZAPI_INSTANCE_ID,
        "ZAPI_TOKEN": ZAPI_TOKEN,
        "ZAPI_CLIENT_TOKEN": ZAPI_CLIENT_TOKEN,
    }
    faltando = [chave for chave, valor in obrigatorias.items() if not valor]
    if faltando:
        log.error("Variaveis de ambiente ausentes no .env: %s", ", ".join(faltando))
        return False
    return True


def buscar_contatos() -> list[dict]:
    """Le os contatos da tabela no Supabase (no maximo LIMITE_ENVIOS)."""
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    resposta = (
        supabase.table(TABELA_CONTATOS)
        .select("nome, telefone")
        .limit(LIMITE_ENVIOS)
        .execute()
    )

    contatos = resposta.data or []
    log.info("Encontrados %d contato(s) no Supabase.", len(contatos))
    return contatos


def enviar_mensagem(nome: str, telefone: str) -> bool:
    """Envia uma mensagem de texto para um numero via Z-API."""
    url = (
        f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}"
        f"/token/{ZAPI_TOKEN}/send-text"
    )

    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN,
    }

    payload = {
        "phone": telefone,
        "message": f"Ola, {nome} tudo bem com voce?",
    }

    try:
        resposta = requests.post(url, json=payload, headers=headers, timeout=30)
        resposta.raise_for_status()
        log.info("Mensagem enviada para %s (%s).", nome, telefone)
        return True
    except requests.exceptions.RequestException as erro:
        log.error("Falha ao enviar para %s (%s): %s", nome, telefone, erro)
        return False


def main() -> None:
    log.info("Iniciando disparo de mensagens b2bflow...")

    if not validar_ambiente():
        log.error("Encerrando: configure o arquivo .env corretamente.")
        return

    contatos = buscar_contatos()
    if not contatos:
        log.warning("Nenhum contato encontrado. Verifique a tabela no Supabase.")
        return

    enviados = 0
    for contato in contatos:
        nome = contato.get("nome")
        telefone = contato.get("telefone")

        if not nome or not telefone:
            log.warning("Contato ignorado (nome ou telefone vazio): %s", contato)
            continue

        if enviar_mensagem(nome, str(telefone)):
            enviados += 1

    log.info("Processo finalizado. %d de %d mensagem(ns) enviada(s).",
             enviados, len(contatos))


if __name__ == "__main__":
    main()