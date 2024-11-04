def div_lista(lista):
    tamanho_lista = len(lista) // 3

    parte1 = lista[:tamanho_lista]
    parte2 = lista[tamanho_lista:2*tamanho_lista]
    parte3 = lista[2*tamanho_lista:]

    return parte1, parte2, parte3

lista  = [1,2,3,4,5,6,7,8,9,10,11,12]

parte1, parte2, parte3 = div_lista(lista)

print(parte1,parte2,parte3)
