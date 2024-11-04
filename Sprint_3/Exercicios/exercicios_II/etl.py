import re
from collections import defaultdict

arquivo = 'Sprint_3/Exercicios/exercicios_II/actors.csv'
txt_1 = 'Sprint_3/Exercicios/exercicios_II/etapa-1.txt'
txt_2 = 'Sprint_3/Exercicios/exercicios_II/etapa-2.txt'
txt_3 = 'Sprint_3/Exercicios/exercicios_II/etapa-3.txt'
txt_4 = 'Sprint_3/Exercicios/exercicios_II/etapa-4.txt'
txt_5 = 'Sprint_3/Exercicios/exercicios_II/etapa-5.txt'

def etapa_1():
    mais_filmes = 0
    ator_max_filmes = ''
    pattern = r'^([^,]+),[^,]+,[\s]*([\d]+),'

    with open(arquivo, 'r', encoding='utf-8') as dados:
        next(dados)  # Pula o cabeçalho
        for linha in dados:
            match = re.match(pattern, linha.strip())
            if match:
                ator = match.group(1).strip()
                filmes = int(match.group(2).strip())

                if filmes > mais_filmes:
                    mais_filmes = filmes
                    ator_max_filmes = ator

    with open(txt_1, 'w', encoding='utf-8') as etapa_1:
        etapa_1.write(f'O ator com mais filmes é {ator_max_filmes}, com {mais_filmes} filmes')

def etapa_2():
    total_receita = 0.0
    registros = 0
    pattern = r',([\d.]+)\s*$'

    with open(arquivo, 'r', encoding='utf-8') as dados:
        next(dados)  # Pula o cabeçalho
        for linha in dados:
            match = re.search(pattern, linha.strip())
            if match:
                receita = float(match.group(1))
                total_receita += receita
                registros += 1

    media_total_receita = total_receita / registros if registros > 0 else 0

    with open(txt_2, 'w', encoding='utf-8') as etapa_2:
        etapa_2.write(f'A média total da receita bruta é {media_total_receita:.2f}')

def etapa_3():
    ator = ''
    maior_media_ator = 0.0
    pattern = r'^"?(.*?)"?\s*,[^,]*\s*,[^,]*\s*,([\d.]+)'

    with open(arquivo, 'r', encoding='utf-8') as dados:
        next(dados)  # Pula o cabeçalho
        for linha in dados:
            match = re.match(pattern, linha.strip())
            if match:
                nome_ator = match.group(1)
                media = float(match.group(2))

                if media > maior_media_ator:
                    ator = nome_ator
                    maior_media_ator = media

    with open(txt_3, 'w', encoding='utf-8') as etapa_3:
        etapa_3.write(f'o ator com maior média é {ator}, com a média de {maior_media_ator:.2f}')

def etapa_4():
    contagem_filmes = defaultdict(int)
    pattern = r'^(?:"[^"]+"|[^,]+),[^,]*,[^,]*,[^,]*,(.*?),'

    with open(arquivo, 'r', encoding='utf-8') as dados:
        next(dados)  # Pula o cabeçalho
        for linha in dados:
            match = re.match(pattern, linha.strip())
            if match:
                filme = match.group(1).strip()
                contagem_filmes[filme] += 1

    ordernar_filmes = sorted(contagem_filmes.items(), key=lambda x: (-x[1], x[0]))

    with open(txt_4, 'w', encoding='utf-8') as etapa_4:
        for i, (filme, contagem) in enumerate(ordernar_filmes, 1):
            etapa_4.write(f'{i} - Filme {filme} aparece {contagem} vez(es) no dataset\n')

def etapa_5():
    atores_receita = []
    pattern = r'^(?:"([^"]+)"|([^,]+)),([\d.]+)'

    with open(arquivo, 'r', encoding='utf-8') as dados:
        next(dados)  # Pula o cabeçalho
        for linha in dados:
            match = re.match(pattern, linha.strip())
            if match:
                nome_ator = match.group(1) if match.group(1) else match.group(2)
                receita_total = float(match.group(3))
                atores_receita.append((nome_ator, receita_total))

    atores_receita.sort(key=lambda x: x[1], reverse=True)

    with open(txt_5, 'w', encoding='utf-8') as etapa_5:
        for nome_ator, receita_total in atores_receita:
            etapa_5.write(f'{nome_ator} - {receita_total:.2f}\n')

# Executar todas as etapas
etapa_1()
etapa_2()
etapa_3()
etapa_4()
etapa_5()
