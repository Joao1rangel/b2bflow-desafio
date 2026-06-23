# Disparo de mensagens no WhatsApp 🚀

E aí! Esse é o meu projeto pro desafio de estágio em Python da **b2bflow**.

A ideia é simples na descrição e divertida de montar: um script em Python que lê uma lista de contatos guardada no **Supabase** e dispara, pra cada um, uma mensagem personalizada no WhatsApp usando a **Z-API**. Tipo um carteiro digital — ele pega os nomes na agenda e entrega a mensagem certinha pra cada pessoa.

A mensagem que sai é essa, com o nome de cada contato no lugar:

> Olá, **\<nome_contato\>** tudo bem com você?

## Como funciona, por cima

O fluxo tem três peças conversando entre si:

1. **Supabase** — é onde os contatos moram (nome + telefone). Funciona como um banco de dados na nuvem.
2. **Python** — o cérebro da operação. Lê os contatos, monta a mensagem e organiza os envios.
3. **Z-API** — a ponte com o WhatsApp. É ela que entrega a mensagem de fato.

```
Supabase (contatos)  ->  Python (main.py)  ->  Z-API  ->  WhatsApp 📱
```

## Tecnologias

- **Python 3**
- **Supabase** (banco de dados PostgreSQL na nuvem)
- **Z-API** (envio de mensagens no WhatsApp)
- Bibliotecas: `supabase`, `requests`, `python-dotenv`

## 1. Montando a tabela no Supabase

Lá no **SQL Editor** do Supabase, rodei este SQL pra criar a tabela `contatos` e já deixar alguns contatos de teste:

```sql
create table contatos (
  id bigint generated always as identity primary key,
  nome text not null,
  telefone text not null
);

insert into contatos (nome, telefone) values
  ('Joao',  '5521999999999'),
  ('Maria', '5521988888888'),
  ('Pedro', '5521977777777');
```

> ⚠️ O telefone precisa estar no formato **DDI + DDD + número**, só dígitos, sem espaço nem traço. Exemplo: `5521999999999`. Foi um detalhe que a Z-API exige e que é fácil esquecer.

## 2. Variáveis de ambiente (.env)

As credenciais ficam todas num arquivo `.env` na raiz do projeto (que **não** vai pro Git — falo mais disso lá embaixo). Pra saber quais variáveis preencher, é só copiar o `.env.example`:

```
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-publishable-key
ZAPI_INSTANCE_ID=seu-instance-id
ZAPI_TOKEN=seu-token
ZAPI_CLIENT_TOKEN=seu-client-token
```

Onde achar cada uma:
- **SUPABASE_URL** e **SUPABASE_KEY** -> no painel do Supabase, em *Project Settings -> API Keys* (use a *publishable key*).
- **ZAPI_INSTANCE_ID** e **ZAPI_TOKEN** -> no painel da Z-API, na sua instância.
- **ZAPI_CLIENT_TOKEN** -> no menu *Segurança* da Z-API (precisa ativar o token de segurança da conta).

## 3. Rodando o projeto

```bash
# (opcional, mas recomendado) criar um ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# instalar as dependencias
pip install -r requirements.txt

# rodar!
python main.py
```

Se tudo estiver certo, o terminal vai mostrar os logs de cada etapa e as mensagens vão chegar no WhatsApp. Algo assim:

```
INFO | Encontrados 3 contato(s) no Supabase.
INFO | Mensagem enviada para Joao (5521999999999).
INFO | Processo finalizado. 3 de 3 mensagem(ns) enviada(s).
```

## Algumas decisões técnicas (e o porquê delas)

Achei que valia explicar algumas escolhas que fiz pelo caminho, porque elas dizem mais sobre como penso do que o código sozinho:

- **Credenciais no `.env` + `.gitignore`:** nada de senha ou token escrito direto no código. Tudo fica no `.env`, que está no `.gitignore` pra nunca subir pro GitHub. No lugar dele, deixei um `.env.example` mostrando *quais* variáveis são necessárias, sem expor os valores — assim quem for rodar o projeto sabe o que preencher.

- **Logs em cada etapa:** em vez de o script rodar mudo, ele vai contando o que está fazendo (quantos contatos achou, pra quem mandou, quantas deram certo). Facilita demais na hora de entender o que aconteceu, ainda mais se algo falhar.

- **Tratamento de erro no envio:** se o envio pra um contato falhar, o script não quebra tudo — ele registra qual contato falhou e por quê, e segue tentando os outros. Achei mais útil garantir que um número errado não derrube o envio inteiro.

- **Sem RLS na tabela (de propósito):** o Supabase tem uma camada de segurança chamada Row Level Security. Deixei desligada porque, pra esse desafio, ela só atrapalharia a leitura dos contatos. Num cenário real de produção, eu ativaria o RLS e configuraria as permissões com cuidado — mas aqui, com dados de teste, optei pela simplicidade.

- **Telefone como texto (e não número):** guardei o telefone como `text` no banco, e não como número, justamente pra não perder o zero nem a formatação que a Z-API espera.

---

Feito com 💜 por **João Pedro Salama Rangel (JPSR)** pro desafio da b2bflow.