# Lista de nomes de animais
animais = ["Cachorro", "Gato", "Elefante", "Leão", "Tigre", "Rinoceronte", 
           "Girafa", "Urso", "Cervo", "Lobo", "Macaco", "Panda", "Zebra", 
           "Canguru", "Tartaruga", "Golfinho", "Baleia", "Pinguim", "Jacaré", "Foca"]

# Ordenar a lista
animais_ordenados = sorted(animais)

# Imprimir cada nome de animal
[print(animal) for animal in animais_ordenados]

# Salvar em um arquivo CSV
with open('animais.csv', 'w') as arquivo:
    for animal in animais_ordenados:
        arquivo.write(f"{animal}\n")
