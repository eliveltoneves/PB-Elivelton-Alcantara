import sys
import os
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.dynamicframe import DynamicFrame
import boto3

# Pegar os argumentos do job parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'input_path', 'output_path'])

input_path = args['input_path']
output_path = args['output_path']

# Configuração do Glue Context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Criação de diretórios no bucket, se necessário
s3 = boto3.client('s3')

# Extrair bucket e prefix do output_path
bucket_name = output_path.split('/')[2]
prefix = '/'.join(output_path.split('/')[3:]) + "CSV/PARQUET/Movies/"

# Criar diretório no S3, se não existir
if not s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix).get('Contents'):
    s3.put_object(Bucket=bucket_name, Key=(prefix if prefix.endswith('/') else prefix + '/'))

# Carregar os dados da camada raw
datasource0 = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [input_path]},
    format="csv",
    format_options={"withHeader": True, "separator": "|"}
)

# Converter DynamicFrame para DataFrame para realizar a filtragem
df = datasource0.toDF()

# Filtrar apenas os filmes do gênero "Drama" ou "Romance" e do ano de 2020
df_filtrado = df.filter(
    (df['genero'].isin('Drama', 'Romance')) & (df['anoLancamento'] == 2020)
)

# Converter de volta para DynamicFrame para salvar no Glue Data Catalog
dynamic_frame_filtrado = DynamicFrame.fromDF(df_filtrado, glueContext, "dynamic_frame_filtrado")

# Gravar os dados na camada trusted
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame_filtrado,
    connection_type="s3",
    connection_options={"path": f"s3://{bucket_name}/{prefix}"},
    format="parquet"
)

# Finalizar o job
job.commit()
