# FastAPI CRUD - Sistema de Inscrições

API completa para gerenciamento de inscrições em faixas etárias, desenvolvida com **FastAPI** seguindo boas práticas de desenvolvimento e arquitetura moderna.

## 🚀 Tecnologias

- **FastAPI** - Framework web moderno e de alta performance
- **PostgreSQL** - Banco de dados relacional robusto
- **Redis** - Cache e filas de processamento assíncrono
- **JWT** - Autenticação segura com tokens
- **SQLAlchemy/SQLModel** - ORM assíncrono
- **Pydantic v2** - Validação de dados
- **Docker & Docker Compose** - Containerização
- **Pytest** - Testes automatizados abrangentes

## 📋 Funcionalidades

- ✅ **CRUD completo** para faixas etárias e inscrições
- ✅ **Autenticação JWT** segura
- ✅ **Validação automática** de idade vs faixa etária
- ✅ **Processamento assíncrono** com Redis
- ✅ **Background workers** para processamento de inscrições
- ✅ **Documentação automática** (Swagger/OpenAPI)
- ✅ **Testes completos** (100% de cobertura dos endpoints)
- ✅ **Logs estruturados** para monitoramento
- ✅ **Arquitetura em camadas** (routers, services, models)

## 🐳 Como executar

### Pré-requisitos
- Docker e Docker Compose instalados

### Execução

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/brenpaiva/crud-fastapi.git
   cd crud-fastapi
   ```

2. **Inicie os serviços:**
   ```bash
   docker-compose up -d
   ```

3. **Acesse a aplicação:**
   - **API**: http://localhost:8000
   - **Documentação interativa**: http://localhost:8000/docs
   - **Redoc**: http://localhost:8000/redoc

## 🔐 Autenticação

A API utiliza **JWT (JSON Web Tokens)** para autenticação segura.

### Credenciais padrão:
- **Username**: `admin`
- **Password**: `secret`

### Como obter um token:

**Via curl:**
```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Usando o token:
```bash
curl -X POST "http://localhost:8000/age-groups/" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{"name": "Infantil", "min_age": 6, "max_age": 12}'
```

## 📡 Endpoints principais

### Autenticação
- `POST /token` - Obter token JWT

### Faixas Etárias
- `GET /age-groups/` - Listar todas as faixas (público)
- `POST /age-groups/` - Criar faixa (🔒 autenticado)
- `GET /age-groups/{id}` - Buscar por ID (público)
- `PUT /age-groups/{id}` - Atualizar (🔒 autenticado)
- `DELETE /age-groups/{id}` - Deletar (🔒 autenticado)

### Inscrições
- `GET /enrollments/` - Listar inscrições (público)
- `POST /enrollments/` - Criar inscrição (🔒 autenticado)
- `GET /enrollments/{id}` - Buscar por ID (público)
- `PATCH /enrollments/{id}/status` - Atualizar status (🔒 autenticado)
- `PUT /enrollments/{id}` - Atualizar completo (🔒 autenticado)
- `DELETE /enrollments/{id}` - Deletar (🔒 autenticado)

### Health Check
- `GET /api/v1/health` - Status da aplicação e banco

## 🗄️ Banco de Dados

### Modelo de dados:

**AgeGroup (Faixas Etárias):**
- `id` (UUID) - Chave primária
- `name` (string) - Nome da faixa (ex: "Infantil")
- `min_age` (int) - Idade mínima inclusiva
- `max_age` (int) - Idade máxima inclusiva

**Enrollment (Inscrições):**
- `id` (UUID) - Chave primária
- `name` (string) - Nome completo do inscrito
- `email` (string) - Email de contato
- `age` (int) - Idade atual
- `age_group_id` (UUID) - FK para faixa etária
- `status` (enum) - Status: pending, approved, rejected

### Regras de negócio:
- A idade do inscrito deve estar dentro dos limites da faixa etária
- Inscrições são criadas com status "pending" por padrão
- Background worker processa automaticamente as aprovações

## 🧪 Testes

O projeto possui **testes abrangentes** cobrindo todos os endpoints e cenários:

```bash
# Executar todos os testes
docker-compose exec api pytest tests/ -v

# Executar com cobertura
docker-compose exec api pytest tests/ --cov=app

# Executar testes específicos
docker-compose exec api pytest tests/test_age_groups.py -v
```

**Cobertura atual: 8/8 testes passando (100% dos endpoints)**

## ⚙️ Configuração

### Variáveis de ambiente (.env):
```env
# Banco de dados
DATABASE_URL=postgresql+asyncpg://postgres:breno123@db:5432/fastapi

# Autenticação
API_USERNAME=admin
API_PASSWORD=secret

# Redis
REDIS_URL=redis://redis:6379/0

# Aplicação
LOG_LEVEL=INFO
INIT_DB=true
```

## 🔄 Background Processing

A aplicação utiliza **Redis** para processamento assíncrono:

- **Filas**: Inscrições são enfileiradas automaticamente após criação
- **Worker**: Processa lotes de inscrições aplicando regras de negócio
- **Status**: Atualiza automaticamente de "pending" para "approved/rejected"

### Executar worker manualmente:
```bash
docker-compose exec api python -m worker.processor
```

## 🏗️ Arquitetura

O projeto segue **boas práticas** de desenvolvimento:

```
app/
├── api/                 # Camada de routers/endpoints
├── core/               # Configurações e segurança
├── db/                 # Sessões de banco
├── models/             # Modelos SQLAlchemy
├── schemas/            # Schemas Pydantic
├── services/           # Lógica de negócio
├── utils/              # Utilitários
└── queue/              # Redis e filas

worker/                 # Background workers
tests/                  # Testes automatizados
```

### Padrões aplicados:
- **Separation of Concerns** - Cada camada tem responsabilidade específica
- **Dependency Injection** - FastAPI DI para sessões e autenticação
- **Async/Await** - Operações assíncronas em toda aplicação
- **Type Hints** - Tipagem completa para melhor manutenibilidade
- **Docstrings** - Documentação inline em funções importantes


