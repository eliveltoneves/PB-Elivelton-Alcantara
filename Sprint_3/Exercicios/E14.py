def teste(*args, **kwargs):
    for arg in args:
        print(arg)
    for kwarg in kwargs.values():
        print(kwarg)

teste(1, 3, 4, 'hello', parametro_nomeado='alguma coisa', x=20)
