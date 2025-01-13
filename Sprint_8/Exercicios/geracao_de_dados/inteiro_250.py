import random

# Gerar lista com 250 números inteiros aleatórios
numeros = [random.randint(1, 1000) for _ in range(250)]

# Inverter a lista
numeros.reverse()

# Imprimir a lista invertida
print(numeros)
