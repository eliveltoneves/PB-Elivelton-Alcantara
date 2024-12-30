import sys
import json
import boto3
from pyspark.context import SparkContext
from awsglue.context import GlueContext # type: ignore
from awsglue.transforms import * # type: ignore
from awsglue.utils import getResolvedOptions # type: ignore
from awsglue.dynamicframe import DynamicFrame # type: ignore
from awsglue.job import Job # type: ignore
from pyspark.sql.functions import col, upper, count, desc

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_TARGET_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Ler o arquivo CSV do S3
input_path = args['S3_INPUT_PATH']
target_path = args['S3_TARGET_PATH']
df = spark.read.csv(input_path, header=True, inferSchema=True)

# Imprimir o schema do DataFrame e salvar como JSON
schema_str = df.schema.json()
with open('/tmp/schema-dataframe.json', 'w') as f:
    f.write(json.dumps({"schema": schema_str}))

df_upper = df.withColumn("nome", upper(col("nome")))

# Salvar contagem total de linhas como JSON
n_linhas = df_upper.count()
with open('/tmp/n_linhas.json', 'w') as f:
    f.write(json.dumps({"total_linhas": n_linhas}))

# Contar e agrupar por ano e sexo, ordenando por ano mais recente
df_grouped = df_upper.groupBy("ano", "sexo").agg(count("*").alias("contagem")).orderBy(desc("ano"))
df_grouped.write.mode("overwrite").json(f"{target_path}/nomes_ano_desc")

# Nome feminino mais frequente
feminino = df_upper.filter(df_upper.sexo == "F") \
    .groupBy("nome", "ano") \
    .agg(count("*").alias("contagem")) \
    .orderBy(desc("contagem")) \
    .first()

with open('/tmp/nomes-feminino-popular.json', 'w') as f:
    f.write(json.dumps({"nome": feminino["nome"], "ano": feminino["ano"], "contagem": feminino["contagem"]}))

# Nome masculino mais frequente
masculino = df_upper.filter(df_upper.sexo == "M") \
    .groupBy("nome", "ano") \
    .agg(count("*").alias("contagem")) \
    .orderBy(desc("contagem")) \
    .first()

with open('/tmp/nomes-masculino-popular.json', 'w') as f:
    f.write(json.dumps({"nome": masculino["nome"], "ano": masculino["ano"], "contagem": masculino["contagem"]}))

# Salvar o DataFrame com nomes em maiúsculo como JSON
df_upper.write.mode("overwrite").json(f"{target_path}/nomes-upper")

# Upload dos arquivos JSON para o S3
s3_client = boto3.client('s3')
bucket_name = target_path.split('/')[2]
key_prefix = '/'.join(target_path.split('/')[3:])

def upload_file_to_s3(file_path, bucket, key):
    s3_client.upload_file(file_path, bucket, key)

upload_file_to_s3('/tmp/schema-dataframe.json', bucket_name, f"{key_prefix}/schema-dataframe.json")
upload_file_to_s3('/tmp/n_linhas.json', bucket_name, f"{key_prefix}/n_linhas.json")
upload_file_to_s3('/tmp/nomes-feminino-popular.json', bucket_name, f"{key_prefix}/nomes-feminino-popular.json")
upload_file_to_s3('/tmp/nomes-masculino-popular.json', bucket_name, f"{key_prefix}/nomes-masculino-popular.json")

job.commit()
