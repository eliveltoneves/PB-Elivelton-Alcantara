import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Configurações
BUCKET_NAME = "desafio-sprint-5"  # Nome único do bucket
REGION = "us-east-1"  # Região onde o bucket será criado
DATASET = "operadora_plano_saude.csv"  # Caminho local do arquivo CSV
S3_OBJECT_NAME = "dados_operadoras_s3.csv"  # Nome do arquivo no bucket S3

def create_s3_bucket(bucket_name, region):
    """Criar um bucket no S3."""
    s3 = boto3.client("s3")
    try:
        print(f"Criando bucket '{bucket_name}' na região '{region}'...")
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )
        print(f"Bucket '{bucket_name}' criado com sucesso.")
        return True
    except ClientError as e:
        print(f"Erro ao criar bucket: {e}")
        return False

def upload_file_to_s3(file_path, bucket_name, object_name):
    """Fazer upload de um arquivo local para o bucket S3."""
    s3 = boto3.client("s3")
    try:
        print(f"Fazendo upload de '{file_path}' para o bucket '{bucket_name}'...")
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"Arquivo enviado com sucesso: s3://{bucket_name}/{object_name}")
        return True
    except FileNotFoundError:
        print(f"Arquivo '{file_path}' não encontrado.")
        return False
    except NoCredentialsError:
        print("Credenciais da AWS não configuradas corretamente.")
        return False
    except ClientError as e:
        print(f"Erro ao fazer upload: {e}")
        return False

def main():
    """Executar todo o processo."""
    # Etapa 1: Criar o bucket
    if not create_s3_bucket(BUCKET_NAME, REGION):
        print("Processo interrompido devido a falha na criação do bucket.")
        return
    
    # Etapa 2: Fazer upload do arquivo local para o bucket
    if not upload_file_to_s3(DATASET, BUCKET_NAME, S3_OBJECT_NAME):
        print("Processo interrompido devido a falha no upload.")
        return
    
    print("Processo concluído com sucesso!")

if __name__ == "__main__":
    main()
