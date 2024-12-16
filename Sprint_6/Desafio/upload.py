import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from datetime import datetime
import os

# Nome do bucket
BUCKET_NAME = "data-lake-elivelton"
# Caminhos dentro do container (volume)
movies_file = "/app/data/movies.csv"
series_file = "/app/data/series.csv"

def create_bucket(bucket_name, region=None):
    """Cria um bucket no S3."""
    try:
        s3_client = boto3.client('s3', region_name=region)
        
        if region:  # Se a região for especificada
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        else:  # Caso contrário, crie sem especificar a configuração
            s3_client.create_bucket(Bucket=bucket_name)
        
        print(f"Bucket '{bucket_name}' criado com sucesso.")
    except ClientError as e:
        print(f"Erro ao criar bucket: {e}")
    except NoCredentialsError:
        print("Credenciais AWS não encontradas.")

def upload_to_s3(local_file_path, bucket, data_type):
    """Faz upload de um arquivo local para o S3 com a estrutura de destino especificada."""
    try:
        # Data de processamento
        today = datetime.now()
        date_path = today.strftime("%Y/%m/%d")

        # Caminho de destino no S3
        s3_path = f"Raw/Local/CSV/{data_type}/{date_path}/{os.path.basename(local_file_path)}"

        s3_client = boto3.client('s3')
        s3_client.upload_file(local_file_path, bucket, s3_path)
        print(f"Arquivo '{local_file_path}' enviado para 's3://{bucket}/{s3_path}'.")
    except ClientError as e:
        print(f"Erro ao enviar arquivo para o S3: {e}")
    except NoCredentialsError:
        print("Credenciais AWS não encontradas.")

if __name__ == "__main__":
    # Criar o bucket (caso não exista)
    create_bucket(BUCKET_NAME)

    # Upload dos arquivos
    upload_to_s3(movies_file, BUCKET_NAME, "Movies")
    upload_to_s3(series_file, BUCKET_NAME, "Series")
