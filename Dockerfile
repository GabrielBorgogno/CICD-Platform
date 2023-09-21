# Use a imagem base do Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requisitos
COPY requirements.txt .

# Instale as dependências com o pip
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
# Instala o módulo psycopg2 ou psycopg
RUN apt-get update && apt-get install -y libpq-dev
# Copie todo o código do aplicativo principal para o diretório de trabalho
COPY . .

# Defina quaisquer comandos adicionais necessários para configurar o aplicativo principal
# Exemplo: migrações de banco de dados, coletar arquivos estáticos, etc.

# Defina o comando de execução padrão
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
