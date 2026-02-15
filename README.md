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

# Benchmark: FastAPI vs. Django Ninja (Async Performance)

Este relatório apresenta uma análise comparativa de desempenho entre duas implementações de uma mesma API de "Lista de Desejos" (Wishlist), utilizando FastAPI e Django Ninja. Ambas as aplicações foram testadas em ambientes isolados utilizando Docker e submetidas a testes de carga com a ferramenta Locust.

## 📊 Resumo dos Resultados (Aggregated)

| Métrica | Django Ninja | FastAPI | Diferença |
| :--- | :--- | :--- | :--- |
| **Requisições Totais** | 6.935 | 4.079* | - |
| **Média de Latência** | 4.76 ms | **4.43 ms** | **FastAPI -6.9%** |
| **Mediana** | 4 ms | **4 ms** | **Empate** |
| **95%ile (Latência)** | 9 ms | **8 ms** | **FastAPI -11.1%** |
| **99%ile (Latência)** | 24.7 ms | **10 ms** | **FastAPI -59.5%** |
| **Vazão (RPS)** | 66.2 | **66.6** | **FastAPI +0.6%** |
| **Falhas** | 0% | 0% | **Estável** |

## 🔍 Análise Técnica
1. Latência e Estabilidade (P99)
O diferencial mais significativo no benchmark foi o 99%ile. Enquanto o Django Ninja apresentou picos de até 24.7ms para os 1% das requisições mais lentas, o FastAPI manteve-se extremamente estável em 10ms. Isso indica uma gestão de loop de eventos (event loop) e serialização de dados (Pydantic V2) altamente eficiente sob carga constante.

2. Eficiência de Vazão (RPS)
Ambos os frameworks atingiram o teto de aproximadamente 66 RPS no ambiente de testes. O ligeiro ganho do FastAPI (66.6) demonstra que, embora a diferença de velocidade bruta seja pequena, o framework consegue processar um volume maior de dados com menor custo computacional por ciclo.

3. Confiabilidade
Ambas as implementações apresentaram 0% de falhas, validando que tanto o Django Ninja quanto o FastAPI, quando implementados de forma assíncrona com drivers de banco de dados adequados (SQLAlchemy Async / Postgres), são perfeitamente capazes de sustentar ambientes de produção de alta concorrência.

### Ambiente de Teste

* **Ferramenta de Stress:** Locust
* **Carga:** 100 usuários simultâneos (Spawn Rate: 10/s)
* **Infraestrutura:** Docker Compose (WSL2 / Windows)
* **Banco de Dados:** PostgreSQL 17.6
* **Servidor ASGI:** Gunicorn com Uvicorn Workers (2 workers)
