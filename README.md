# CRUD-FASTAPI

API para gerenciamento de inscrições em eventos esportivos, com autenticação JWT, banco de dados PostgreSQL, processamento assíncrono com Redis e Docker.

## Tecnologias

- Python 3.13, FastAPI, SQLModel, Pydantic
- PostgreSQL 15, Redis 7
- Docker e Docker Compose
- Pytest para testes

## Como rodar

1. Clone o repositório:
   ```bash
   git clone https://github.com/brenpaiva/crud-fastapi.git
   cd crud-fastapi
   ```

2. Suba os serviços com Docker:
   ```bash
   docker compose up -d
   ```

3. Acesse:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## Autenticação

- JWT (HS256)
- Credenciais padrão:
  ```
  Username: admin
  Password: supersecretkey
  ```

Para obter token:
```bash
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=supersecretkey"
```

## Endpoints principais

- `POST /token` — autenticação
- `GET /age-groups/` — listar faixas etárias
- `POST /age-groups/` — criar faixa (autenticado)
- `GET /enrollments/` — listar inscrições
- `POST /enrollments/` — criar inscrição (autenticado)

## Banco de dados

- Tabelas: `age_groups` (faixas etárias), `enrollments` (inscrições)
- Relacionamento 1:N entre faixas e inscrições

## Variáveis de ambiente (.env)

Veja o arquivo `.env` para configurações de banco, Redis, JWT e credenciais.

## Testes

Execute:
```bash
docker compose exec api pytest -v
```

## Contribuição

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit e push
4. Abra um Pull Request

## Licença

MIT


