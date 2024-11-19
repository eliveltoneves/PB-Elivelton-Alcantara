def conta_vogais(texto:str)-> int:
    is_vogal = lambda x: x.lower() in 'aeiou'
    vogais= filter(is_vogal, texto)
    return len(list(vogais))
    