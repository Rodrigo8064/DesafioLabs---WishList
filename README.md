# 🚀 Wishlist - Django Ninja Async Pro
Esta é uma API de alta performance desenvolvida com Django Ninja, focada em operações assíncronas nativas. O projeto utiliza uma arquitetura Stateless (JWT), removendo middlewares síncronos pesados do Django para garantir latência mínima e escalabilidade.

🛠 Tecnologias Principais
* **Framework:** Django 5.1+
* **API Engine:** Django Ninja (Async)
* **Servidor ASGI:** Uvicorn / Gunicorn
* **Banco de Dados:** PostgreSQL 17
* **Containerização:** Docker & Docker Compose
* **Gerenciador de Dependências:** Poetry
* **Auth:** JWT (JSON Web Tokens)

---

## 🏗 Como Rodar o Projeto

### Pré-requisitos
* Docker instalado
* Docker Compose instalado

### 1. Clonar o Repositório
```bash
git clone https://github.com/Rodrigo8064/DesafioLabs_WishList.git
cd seu-repositorio
```

### 2. Configurar o Ambiente
Crie um arquivo .env na raiz do projeto seguindo o modelo abaixo:
```bash
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=sua-chave-secreta
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
```
### 3. Subir os Containers
O comando abaixo irá construir a imagem, rodar as migrações automaticamente e subir o servidor:

```Bash
docker-compose up --build
```
# 🚦 Primeiros Passos
Após subir os containers, a API estará disponível em http://localhost:8000.

### 1. Criar um Usuário
Como a API é protegida, o primeiro passo é criar um usuário através da rota de cadastro:

POST /api/users/

### 2. Obter o Token JWT
Faça o login para receber o seu Bearer Token:

POST /api/auth/login/

Guarde o access_token retornado.

### 3. Utilizar a API
Para acessar as rotas protegidas (Produtos, Favoritos, etc.), envie o token no Header das requisições:

```HTTP
Authorization: Bearer SEU_TOKEN_AQUI
```
### 4. Documentação Interativa
Você pode testar todas as rotas diretamente pelo Swagger:

Swagger UI: http://localhost:8000/api/docs

# ⚡ Diferenciais de Performance
Middleware Minimalista: Removidos SessionMiddleware e AuthenticationMiddleware para evitar I/O desnecessário.

Async ORM: Todas as queries utilizam aget, acreate, adelete e prefetch_related para não bloquear o Event Loop.

Docker Optimized: Build multi-stage baseado em Alpine Linux para imagens leves e rápidas.

