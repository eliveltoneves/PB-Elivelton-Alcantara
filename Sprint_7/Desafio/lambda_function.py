import os
import requests
import json
from datetime import datetime
import boto3

# Configurações
from chave_tmdb import TMDB_API_KEY  # Chave da API de um arquivo separado
TMDB_BASE_URL = "https://api.themoviedb.org/3"
BUCKET_NAME = "data-lake-elivelton"

# Inicializar o cliente S3
s3_client = boto3.client('s3')

def fetch_tmdb_data(endpoint, params):
    """Faz uma requisição para a API do TMDB."""
    params['api_key'] = TMDB_API_KEY
    response = requests.get(f"{TMDB_BASE_URL}/{endpoint}", params=params)
    response.raise_for_status()
    return response.json()

def save_to_s3(data, file_name):
    """Salva os dados em um arquivo JSON no S3."""
    today = datetime.now()
    date_path = today.strftime("%Y/%m/%d")

    # Caminho no S3
    s3_path = f"Raw/TMDB/JSON/{date_path}/{file_name}"

    # Salvar o arquivo diretamente no S3
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_path,
        Body=json.dumps(data, ensure_ascii=False),
        ContentType='application/json'
    )
    print(f"Arquivo salvo no S3: s3://{BUCKET_NAME}/{s3_path}")

def fetch_and_save_movies_by_genre(year, genre_id):
    """Busca filmes por gênero e ano de lançamento e salva no S3."""
    page = 1
    part = 1

    while True:
        print(f"Buscando página {page} para o gênero {genre_id} no ano {year}...")
        data = fetch_tmdb_data("discover/movie", {
            "language": "en-US",
            "page": page,
            "with_genres": genre_id,
            "primary_release_date.gte": f"{year}-01-01",
            "primary_release_date.lte": f"{year}-12-31"
        })

        results = data.get("results", [])

        if not results:
            break

        # Filtrar os campos necessários
        filtered_results = []
        for movie in results:
            movie_id = movie.get("id")

            # Obter informações detalhadas do filme
            movie_details = fetch_tmdb_data(f"movie/{movie_id}", {"language": "en-US"})

            filtered_results.append({
                "id": movie_details.get("id"),
                "popularity": movie_details.get("popularity"),
                "budget": movie_details.get("budget"),
                "revenue": movie_details.get("revenue"),
                "production_companies": movie_details.get("production_companies"),
                "production_countries": movie_details.get("production_countries"),
                "reviews": movie_details.get("vote_count"),
                "watch/providers": fetch_tmdb_data(f"movie/{movie_id}/watch/providers", {"language": "en-US"}).get("results")
            })

        # Agrupar em arquivos de até 100 registros
        for i in range(0, len(filtered_results), 100):
            chunk = filtered_results[i:i+100]
            file_name = f"tmdb_data_{part}.json"
            save_to_s3(chunk, file_name)
            part += 1

        total_pages = data.get("total_pages", 1)
        if page >= total_pages:
            break

        page += 1

def lambda_handler(event, context):
    """Função Lambda principal."""
    year = 2020

    # Processar os gêneros separadamente
    genres = [18, 10749]  # Drama (18) e Romance (10749)

    for genre_id in genres:
        fetch_and_save_movies_by_genre(year, genre_id)

    return {"statusCode": 200, "body": "Dados processados e salvos com sucesso no S3."}
