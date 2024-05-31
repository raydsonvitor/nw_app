def Zero_adder(n):
    n = int(n)
    try:
        if n > 9:
            return f'{n}'
        else:
            return f'0{n}'
    except:
        print(f'Ocorreu um erro na função Zero_adder em defsofdefs.py. Retornando {n}.')
        return n