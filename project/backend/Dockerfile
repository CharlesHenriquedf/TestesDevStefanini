# Usar a imagem oficial do Python 3.9 slim
FROM python:3.9-slim

# Definir variáveis de ambiente para evitar a criação de arquivos pyc e garantir logs sem buffer
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Configurar o PYTHONPATH para incluir o diretório de trabalho no caminho de importação
ENV PYTHONPATH=/app

# Copiar o arquivo de requisitos para o contêiner
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Expor a porta 8000
EXPOSE 8000

# Comando para executar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
