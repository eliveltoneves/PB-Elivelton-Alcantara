import requests
import pandas as pd
from IPython.display import display
from chaves.chave_tmd import chave_tmdb

api_key = chave_tmdb
url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}&language=pt-BR" # CHAVE EM UM ARQIVO SEPARADO PARA RESPEITAR POLITICAS DE SEGURANÇA WEB

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    filmes = []
    for movie in data['results']:
        filme = {
            'Título': movie['title'],
            'Data de lançamento': movie['release_date'],
            'Visão geral': movie['overview'],
            'Votos': movie['vote_count'],
            'Média de votos': movie['vote_average']
        }
        filmes.append(filme)
    
    # Crie o DataFrame com suporte para caracteres especiais
    df = pd.DataFrame(filmes)

    # Garanta que o pandas use o encoding correto
    display(df)
else:
    print(f"Erro na API: {response.status_code}")
