from datetime import datetime
from CTkMessagebox import CTkMessagebox
from requests import get ,ConnectionError, Timeout

profissionais = ['VITOR', 'RIBEIRO', 'KAUAN', 'FREE2']
despesas = ['CONSUMÍVEIS', 'ALUGUEL', 'ÁGUA', 'LUZ', 'INTERNET','FUNDOS', 'ESTORNO', 'OUTRO']
form_pgmt_saida = ['DINHEIRO', 'BANCO', 'CARTÃO']
form_pgmt_entrada = ['DINHEIRO', 'PIX QR', 'DÉBITO', 'CRÉDITO','PIX CHAVE','MENSAL']
valor_limite_entrada = valor_limite_saida = 9999

def check_datatime_before_run_app():
    #get last datetime & tratar it
    with open(r'txts\last_datetime.txt', 'r') as a:
        last_datetime = datetime.strptime(a.readline(), '%Y-%m-%d')
    #get current datetime
    current_datetime = datetime.today()
    current_datetime = current_datetime.strftime('%Y-%m-%d')
    current_datetime = datetime.strptime(current_datetime, '%Y-%m-%d')
    #compare both
    if current_datetime < last_datetime:
        return False
    else:
        if current_datetime > last_datetime:
            #reescrever arquivo txt
            with open(r'txts\last_datetime.txt', 'w') as a:
                a.write(current_datetime.strftime('%Y-%m-%d'))
                print(f'last datetime atualizado: {current_datetime}')
        return True

def Check_entrada(profissional, meiopgmt, entrada, servicos, bebidas, produtos):#checkar inputs da area de registro de entradas
    algumacoisa = False
    if servicos != '' and profissional == '':#ao selecionar um serviço o usuario deve selecionar o profissional
        print('Opção escolhida ''profissional'' não foi aceita')
        msg = 'Verifique a opção Profissional e tente novamente!'.upper()
        CTkMessagebox(title='Não foi possível Registrar a Entrada', message=msg, icon='cancel')
        return [False, 'profissional']
    if '+' in meiopgmt:#caso haja 2 form de pgmt
        meiospgmt = meiopgmt.split(' + ')
        meiopgmt1 = meiospgmt[0]
        meiopgmt2 = meiospgmt[1]
        entradas = entrada.split(' + ')
        entrada1 = entradas[0]
        entrada2 = entradas[1]
        if meiopgmt1 not in form_pgmt_entrada:
            print('Opção escolhida ''forma de pagamento 1'' não foi aceita')
            msg = 'Verifique a opção Forma de Pagamento 1 e tente novamente!'.upper()
            CTkMessagebox(title='Não foi possível Registrar a Entrada', message=msg, icon='cancel')
            return [False, 'meiopgmt1']
        if entrada1 == '' or str(entrada1).replace('.','').isnumeric()==False or float(entrada1) > valor_limite_entrada or float(entrada1) <= 0:
            print('Opção escolhida ''Valor 1'' não foi aceita')
            msg = 'Verifique a opção Valor 1 e tente novamente!'.upper()
            CTkMessagebox(title='Não foi possível Registrar a Entrada', message=msg, icon='cancel')
            return [False, 'valor1'] 
        if meiopgmt2 not in form_pgmt_entrada:
            print('Opção escolhida ''forma de pagamento 2'' não foi aceita')
            msg = 'Verifique a opção Forma de Pagamento 2 e tente novamente!'.upper()
            CTkMessagebox(title='Não foi possível Registrar a Entrada', message=msg, icon='cancel')
            return [False, 'meiopgmt2']
        if entrada2 == '' or str(entrada2).replace('.','').isnumeric()==False or float(entrada2) > valor_limite_entrada or float(entrada2) <= 0:
            print('Opção escolhida ''Valor 2'' não foi aceita')
            msg = 'Verifique a opção Valor 2 e tente novamente!'.upper()
            CTkMessagebox(title='Não foi possível Registrar a Entrada', message=msg, icon='cancel')
            return [False, 'valor2']
    else:#caso haja so 1 form pgmt
        if meiopgmt not in form_pgmt_entrada:
            print('Opção escolhida ''forma de pagamento'' não foi aceita')
            msg = 'Verifique a opção Forma de Pagamento e tente novamente!'.upper()
            CTkMessagebox(title='Não foi possível Registrar a Entrada', message=msg, icon='cancel')
            return [False, 'meiopgmt1']
        if entrada == '' or str(entrada).replace('.','').isnumeric()==False or float(entrada) > valor_limite_entrada or float(entrada) <= 0:
            print('Opção escolhida ''Valor'' não foi aceita')
            msg = 'Verifique a opção Valor e tente novamente!'.upper()
            CTkMessagebox(title='Não foi possível Registrar a Entrada', message=msg, icon='cancel')
            return [False, 'valor1']

    if servicos != '':
        algumacoisa = True
    if bebidas != '':
        algumacoisa = True
    if produtos != '':
        algumacoisa = True

    if algumacoisa == True:
        return True
    else:
        print('Nenhum serviço, bebida ou produto selecionado.')
        msg = 'Selecione um serviço, bebida ou produto e tente novamente!'.upper()
        CTkMessagebox(title='Não foi possível Registrar a Entrada', message=msg, icon='cancel')
        return False

def Check_saida(despesa, meiopgmt, saida):#checkar inuts da area de registro de saidas
    if despesa not in despesas:
        print('Opção escolhida ''despesa'' não foi aceita')
        msg = 'Verifique a opção Despesa e tente novamente!'.upper()
        CTkMessagebox(title='Não foi possível Registrar a Saída', message=msg, icon='cancel')
        return [False, 'despesa']
    if meiopgmt not in form_pgmt_saida:
        print('Opção escolhida ''forma de pagamento'' não foi aceita')
        msg = 'Verifique a opção Forma de Pagamento e tente novamente!'.upper()
        CTkMessagebox(title='Não foi possível Registrar a Entrada', message=msg, icon='cancel')
        return [False, 'meiopgmt']
    if saida == '' or str(saida).replace('.','').isnumeric()==False or float(saida) > valor_limite_saida or float(saida) <= 0:
        print('Opção escolhida ''Valor'' não foi aceita')
        msg = 'Verifique a opção Valor e tente novamente!'.upper()
        CTkMessagebox(title='Não foi possível Registrar a Entrada', message=msg, icon='cancel')
        return [False, 'valor']
    return True

def check_internet_connection():
    try:
        # Tenta fazer uma requisição para o Google
        response = get("http://www.google.com", timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except ConnectionError:
        return False
    except Timeout:
        return False