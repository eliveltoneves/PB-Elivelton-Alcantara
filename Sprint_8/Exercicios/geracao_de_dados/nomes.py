import random
import names

# Definir os parâmetros
random.seed(40)
qtd_nomes_unicos = 3000
qtd_nomes_aleatorios = 10000000

# Gerar nomes únicos
aux = [names.get_full_name() for _ in range(qtd_nomes_unicos)]

# Gerar nomes aleatórios
print(f"Gerando {qtd_nomes_aleatorios} nomes aleatórios...")
dados = [random.choice(aux) for _ in range(qtd_nomes_aleatorios)]

# Salvar nomes no arquivo
with open('nomes_aleatorios.txt', 'w') as arquivo:
    for nome in dados:
        arquivo.write(f"{nome}\n")

print("Arquivo 'nomes_aleatorios.txt' gerado com sucesso!")
