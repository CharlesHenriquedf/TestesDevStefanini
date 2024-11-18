Descrição Geral
Um sistema simples para registro de usuários, login, busca de filmes e histórico de pesquisas. A aplicação possui um backend desenvolvido em FastAPI e um frontend em React, integrado com Axios para comunicação com a API.

Funcionalidades Principais
Registro de Usuário:
Endpoint para registrar novos usuários.
Campos necessários: username, email, password.
Login:
Autentica um usuário registrado.
Retorna um token JWT para autorizar acessos protegidos.
Busca de Filmes:
Pesquisa filmes com base em palavras-chave.
Exibe os resultados em uma lista.
Histórico de Pesquisas:
Mostra todas as buscas realizadas pelo usuário em uma tabela formatada.
Exibe colunas: Título do Filme e Data da Busca.

Estrutura do Projeto
project
├── backend
│   ├── app
│   │   ├── api
│   │   │   ├── dependencies.py
│   │   │   └── endpoints
│   │   │       ├── auth.py
│   │   │       ├── history.py
│   │   │       └── movies.py
│   │   ├── core
│   │   │   ├── logger.py
│   │   │   └── settings.py
│   │   ├── main.py
│   │   ├── models
│   │   │   ├── history.py
│   │   │   └── user.py
│   │   ├── schemas
│   │   │   ├── history.py
│   │   │   └── user.py
│   │   ├── tests
│   │   │   └── test_security.py
│   │   └── utils
│   │       └── external_api.py
│   ├── Dockerfile
│   ├── logs
│   │   ├── app
│   │   ├── endpoints
│   │   ├── schemas
│   │   └── utils
│   ├── README.md
│   └── requirements.txt
├── docker-compose.yml
├── frontend
│   ├── package.json
│   ├── package-lock.json
│   ├── public
│   │   └── index.html
│   ├── README.md
│   └── src
│       ├── api.js
│       ├── App.js
│       ├── components
│       │   ├── HistoryPage.css
│       │   ├── HistoryPage.jsx
│       │   └── HomePage.jsx
│       ├── History.js
│       ├── index.js
│       ├── MovieSearch.js
│       └── styles
│           └── global.css
└── README.md

Configuração e Inicialização
1. Pré-requisitos
Certifique-se de ter instalados:
Docker e Docker Compose
Node.js e npm/yarn (opcional para executar localmente o frontend)

2. Configuração do Backend
Arquivo backend/Dockerfile

# Usar a imagem oficial do Python 3.9 slim
FROM python:3.9-slim

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Diretório de trabalho no contêiner
WORKDIR /app

# Copiar arquivos necessários
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expor a porta do backend
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

Arquivo backend/requirements.txt

fastapi
pydantic
uvicorn
motor
python-jose
passlib


3. Configuração do Frontend
Arquivo frontend/Dockerfile

# Usar a imagem oficial do Node.js
FROM node:16-slim

# Diretório de trabalho no contêiner
WORKDIR /app

# Instalar dependências e construir a aplicação
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Expor a porta do frontend
EXPOSE 3000

# Comando para iniciar o servidor
CMD ["npm", "start"]


4. Arquivo docker-compose.yml

version: '3.8'

services:
  backend:
    build:
      context: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend/logs:/app/logs
    environment:
      - MONGODB_URI=mongodb://mongo:27017/mydatabase
      - SECRET_KEY=your-secret-key
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
    depends_on:
      - mongo

  frontend:
    build:
      context: ./frontend
    ports:
      - "3000:3000"

  mongo:
    image: mongo:5.0
    container_name: mongo
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:


5. Subir os Contêineres
No diretório principal do projeto (onde está o arquivo docker-compose.yml), execute:

docker-compose up --build
Construir as imagens do backend e frontend.
Subir os contêineres para o MongoDB, backend e frontend.

6. Acessando a Aplicação
Frontend: Acesse http://localhost:3000
Backend (API): Acesse http://localhost:8000/docs para a documentação Swagger.

Testando no Insomnia/Postman
Endpoints
Registrar Usuário
Método: POST
URL: http://localhost:8000/auth/register
Body (JSON):

{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "password123"
}


Login
Método: POST
URL: http://localhost:8000/auth/login
Body (JSON):

{
  "email": "testuser@example.com",
  "password": "password123"
}


Buscar Filmes
Método: GET
URL: http://localhost:8000/search?query=movie_name
Headers:

{
  "Authorization": "Bearer <token>"
}


Histórico
Método: GET
URL: http://localhost:8000/history
Headers:

{
  "Authorization": "Bearer <token>"
}



Estilização
Tela azul petróleo com elementos brancos.
Centralização de formulários.
Histórico em tabela bem formatada.

Logs
Local dos logs: backend/logs/
Logs de erros e requisições do backend.

