import random


random_list = random.sample(range(500), 50)


valor_minimo = min(random_list)
valor_maximo = max(random_list)


media = sum(random_list) / len(random_list)


random_list.sort()
n = len(random_list)
if n % 2 == 0:
    mediana = (random_list[n // 2 - 1] + random_list[n // 2]) / 2
else:
    mediana = random_list[n // 2]

print(f'Media: {media}, Mediana: {mediana}, Mínimo: {valor_minimo}, Máximo: {valor_maximo}')
