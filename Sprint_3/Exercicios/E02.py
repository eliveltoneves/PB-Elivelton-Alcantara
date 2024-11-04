numeros = []

for i in range(3):
    numero = [10, 15, 22][i]
    numeros.append(numero)
    
    if numero % 2 == 0:
        print(f"Par: {numero}")
    else: 
        print(f"Ímpar: {numero}")
        