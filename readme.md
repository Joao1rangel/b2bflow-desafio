# Desafio b2bflow — Disparo de mensagens via WhatsApp

Projeto em Python que lê contatos cadastrados no **Supabase** e envia, via **Z-API**,
a mensagem personalizada: `Olá, <nome_contato> tudo bem com você?`

## Tecnologias
- Python 3
- Supabase (banco de dados)
- Z-API (envio de mensagens no WhatsApp)

## 1. Setup da tabela no Supabase

Crie uma tabela chamada `contatos` com os campos abaixo. Você pode rodar este SQL
no **SQL Editor** do Supabase:

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

> O telefone deve estar no formato **DDI + DDD + número**, só dígitos (ex.: `5521999999999`).

## 2. Variáveis de ambiente (.env)

Crie um arquivo `.env` na raiz do projeto (use o `.env.example` como base):

```
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon
ZAPI_INSTANCE_ID=seu-instance-id
ZAPI_TOKEN=seu-token
ZAPI_CLIENT_TOKEN=seu-client-token
```

## 3. Como rodar

```bash
# (recomendado) criar e ativar um ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# instalar as dependências
pip install -r requirements.txt

# executar
python main.py
```

O script lê até 3 contatos da tabela e envia a mensagem para cada número,
exibindo logs do andamento no terminal.