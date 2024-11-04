def soma_valores(numeros_str):
    numeros = [int(num) for num in numeros_str.split(',')]
    return sum(numeros)

numeros_str = '1,3,4,6,10,76'

soma = soma_valores(numeros_str)
print(soma)
