# Imagem base
FROM python:3.9

# Diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos locais para o container
COPY . /app

# Instalar as dependências necessárias
RUN pip install boto3 pandas

# Comando padrão ao iniciar o container
CMD ["python", "upload.py"]
