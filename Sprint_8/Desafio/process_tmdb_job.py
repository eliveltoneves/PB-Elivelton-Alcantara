import sys
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import date_format, col
from datetime import datetime

# Contexto do Glue
glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

# Obter os parâmetros passados no job
args = getResolvedOptions(sys.argv, ["input_path", "output_path"])
input_path = args["input_path"]
output_path = args["output_path"]

# Ler os dados JSON da camada Raw
df = spark.read.format("json").load(input_path)

# Obter a data de modificação mais recente (simula a data de ingestão)
file_metadata = spark.sparkContext._jvm.org.apache.hadoop.fs.Path(input_path)
fs = spark.sparkContext._jvm.org.apache.hadoop.fs.FileSystem.get(file_metadata.toUri(), spark._jsc.hadoopConfiguration())

file_statuses = fs.listStatus(file_metadata)
ingestion_date = max([status.getModificationTime() for status in file_statuses])

# Converter timestamp para o formato YYYY/MM/DD
partition_date = datetime.fromtimestamp(ingestion_date / 1000).strftime("%Y/%m/%d")

# Criar o caminho de saída no formato especificado
output_path_partitioned = f"{output_path}TMDB/PARQUET/Movies/{partition_date}"

# Salvar na camada Trusted em formato Parquet
df.write.mode("overwrite").parquet(output_path_partitioned)
