# Leitura dos números a partir do arquivo
with open("Sprint_4/Exercicios/number.txt", "r") as file:
    number = list(map(int, file.readlines()))

# Filtrando apenas os números pares e ordenando em ordem decrescente
pares = sorted(filter(lambda x: x % 2 == 0, number), reverse=True)

# Selecionando os 5 maiores números pares
maiores_pares = pares[:5]

# Calculando a soma dos 5 maiores números pares
soma_maiores_pares = sum(maiores_pares)

# Exibindo os resultados
print(maiores_pares)
print(soma_maiores_pares)
