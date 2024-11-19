import csv

def processar_notas():
    # Abre o arquivo estudantes.csv para leitura, sem cabeçalho
    with open("Sprint_4/Exercicios/estudantes.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        # Processa cada linha do arquivo CSV
        estudantes = []
        for row in reader:
            # O nome do estudante é o primeiro elemento da linha
            nome = row[0]
            # As notas são os próximos elementos, convertendo para inteiros
            notas = list(map(int, row[1:]))
            
            # Ordena as notas em ordem decrescente e seleciona as três maiores
            tres_maiores_notas = sorted(notas, reverse=True)[:3]
            
            # Calcula a média das três maiores notas com duas casas decimais
            media = round(sum(tres_maiores_notas) / 3, 2)
            
            # Adiciona o resultado ao relatório
            estudantes.append((nome, tres_maiores_notas, media))
        
        # Ordena o resultado pelo nome do estudante
        estudantes.sort(key=lambda x: x[0])

        # Exibe o relatório conforme o formato desejado
        for estudante in estudantes:
            nome, notas, media = estudante
            print(f"Nome: {nome} Notas: {notas} Média: {media}")

# Chama a função para processar e exibir as notas
processar_notas()

