import sys
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from awsglue.context import GlueContext # type: ignore
from awsglue.utils import getResolvedOptions # type: ignore
from awsglue.job import Job # type: ignore
from pyspark.sql.functions import col, explode_outer, lit, coalesce

# Configuração do Glue e Spark
glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

# Obter argumentos de entrada
args = getResolvedOptions(sys.argv, ["JOB_NAME", "trusted_csv_path", "trusted_tmdb_path", "refined_path"])
trusted_csv_path = args["trusted_csv_path"]
trusted_tmdb_path = args["trusted_tmdb_path"]
refined_path = args["refined_path"]

# Inicializar o Job do Glue
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Carregar dados Trusted
df_csv = spark.read.parquet(trusted_csv_path)
df_tmdb = spark.read.parquet(trusted_tmdb_path)

# Unir os dados
df_combined = df_csv.join(df_tmdb, df_csv["id"] == df_tmdb["imdb_id"], "inner")

# Extrair dados de provedores apenas do Brasil (BR)
if "watch/providers" in df_combined.columns:
    # Acessar diretamente a região do Brasil (BR)
    df_combined = df_combined.withColumn("br_providers", col("watch/providers.BR"))
    
    # Explodir as categorias dentro da região BR
    for category in ["ads", "buy", "flatrate", "free", "rent"]:
        df_combined = df_combined.withColumn(
            f"watch_{category}_br",
            explode_outer(col(f"br_providers.{category}"))  # Explodir a categoria específica
        )
        df_combined = df_combined.withColumn(
            f"provider_name_{category}_br",
            coalesce(col(f"watch_{category}_br.provider_name"), lit("Sem Informações"))
        ).withColumn(
            f"display_priority_{category}_br",
            coalesce(col(f"watch_{category}_br.display_priority"), lit(-1))
        ).drop(f"watch_{category}_br")

# Explodir e renomear production_companies
if "production_companies" in df_combined.columns:
    df_combined = df_combined.withColumn(
        "production_companies_exploded",
        explode_outer(col("production_companies"))
    )
    df_combined = df_combined.withColumn(
        "empresa_producao", coalesce(col("production_companies_exploded.name"), lit("Sem Informações"))
    ).drop("production_companies", "production_companies_exploded")

# Explodir e renomear production_countries
if "production_countries" in df_combined.columns:
    df_combined = df_combined.withColumn(
        "production_countries_exploded",
        explode_outer(col("production_countries"))
    )
    df_combined = df_combined.withColumn(
        "pais_producao", coalesce(col("production_countries_exploded.name"), lit("Sem Informações"))
    ).drop("production_countries", "production_countries_exploded")

# Limpeza e transformação de colunas
df_transformed = (
    df_combined
    .fillna("Sem Informações", subset=["empresa_producao", "pais_producao"])
    .withColumnRenamed("id", "id_filme")
    .withColumnRenamed("tituloPincipal", "nome_filme")
    .withColumnRenamed("anoLancamento", "ano_lancamento")
    .withColumnRenamed("tempoMinutos", "tempo_minutos")
    .withColumnRenamed("gênero", "genero")
    .withColumnRenamed("notaMedia", "nota_media")
    .withColumnRenamed("numeroVotos", "numero_votos")
    .withColumnRenamed("generoArtista", "genero_artista")
    .withColumnRenamed("nomeArtista", "nome_artista")
    .withColumnRenamed("Budget", "orcamento")
    .withColumnRenamed("popularity", "popularidade")
    .withColumnRenamed("revenue", "receita")
    .drop("tituloOriginal", "anoNascimento", "anoFalecimento", "profissao", "titulosMaisConhecidos", "watch/providers")
    .dropDuplicates(["id_filme"])
)

# Salvar os dados refinados na camada Refined
refined_path_partitioned = f"{refined_path}/Movies"
df_transformed.write.mode("overwrite").partitionBy("ano_lancamento").parquet(refined_path_partitioned)

# Criação do modelo dimensional
# Tabela Dimensão - Filmes
dim_filmes = df_transformed.select(
    "id_filme", "nome_filme", "nome_artista", "ano_lancamento", "tempo_minutos", "genero", "genero_artista"
).distinct()
dim_filmes.write.mode("overwrite").parquet(f"{refined_path}/dim_filmes")

# Tabela Dimensão - Produção
dim_producao = df_transformed.select(
    "id_filme", "empresa_producao", "pais_producao"
).distinct()
dim_producao.write.mode("overwrite").parquet(f"{refined_path}/dim_producao")

# Tabela Dimensão - Provedores (Brasil)
dim_provedores_br = df_transformed.select(
    "id_filme",
    "provider_name_ads_br", "display_priority_ads_br",
    "provider_name_buy_br", "display_priority_buy_br",
    "provider_name_flatrate_br", "display_priority_flatrate_br",
    "provider_name_free_br", "display_priority_free_br",
    "provider_name_rent_br", "display_priority_rent_br"
).distinct()
dim_provedores_br.write.mode("overwrite").parquet(f"{refined_path}/dim_provedores_br")

# Tabela Fato
fato_filmes = df_transformed.select(
    "id_filme", "orcamento", "receita", "nota_media", "numero_votos", "popularidade"
)
fato_filmes.write.mode("overwrite").parquet(f"{refined_path}/fato_filmes")

# Finalizar o job do Glue
print("Processo concluído com sucesso!")
job.commit()
