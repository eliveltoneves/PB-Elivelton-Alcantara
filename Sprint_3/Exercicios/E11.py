import json

with open('exercicios\person.json', 'r') as file:
    texto = json.load(file)

print(texto)
