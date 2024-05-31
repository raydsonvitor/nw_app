def format_to_float(valor):
    try:
        valor = str(valor).replace(',', '.')
        return float(valor)
    except Exception as e:
        print(f'erro na formatação para numero float: {e}. retorando 0')
        return 0

def format_to_moeda(valor):
    valor = str(valor).replace(',', '.')
    valor = f'{float(valor):.2f}'
    return valor