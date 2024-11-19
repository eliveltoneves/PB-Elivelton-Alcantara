import hashlib

while True:
    user_input = input("Digite uma palavra para mascarar (ou 'sair' para encerrar): ")
    if user_input.lower() == 'sair':
        break
    hash_object = hashlib.sha1(user_input.encode())
    hex_dig = hash_object.hexdigest()
    print("Hash SHA-1:", hex_dig)
