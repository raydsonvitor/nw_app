from customtkinter import *
from tkinter.ttk import Spinbox
from CTkSpinbox import *
import openpyxl as op
from datetime import date
from CTkMessagebox import CTkMessagebox
from time import sleep
from defs_2_0 import *

def Futrica():
    wb=op.load_workbook(r'excell\nw_barbearia_2024.xlsx')
    ws=wb['07-24']

    for item in range(ws.max_row-1):
        celula = ws.cell(row=item+2, column=3)
        valor = celula.value
        if valor == 'VTR':
            valor = 'VITOR'
        celula.value = valor
        print(celula.value)    

    wb.save(r'excell\nw_barbearia_2024.xlsx')

def get_bebidas_fat_semanal(data, periodo):
    def Get_meses_lista_datas_semana(lista_datas):
        #formar lista dos meses diferentes separando-os dos dias e tratando-os
        meses = []
        last_mes = ''
        for data in lista_datas:
            data_splited = data.split('-')
            mes = data_splited[1]
            if last_mes != mes:
                meses.append(mes)
            last_mes = mes
        return meses # [atual] | [antigo, atual]
    #try:
    #definições importantes
    data_splited = data.split('-')
    mes_data = data_splited[1]
    periodo_splited = periodo.split('-')
    ano = '20' + periodo_splited[1]
    ano_abrev = periodo_splited[1]
    #obtenção das datas da semana
    if Check_datas(data) == False:#check se as datas da semana são válidas para a data atual
        Update_lista_datas_semana(data, ano)#atualiza as datas da semana
        lista_datas = Get_lista_datas_semana()
    else:
        lista_datas = Get_lista_datas_semana() 
    #calculando o faturamento de cada profissional no(s) periodo(s)
    lista_meses = Get_meses_lista_datas_semana(lista_datas)#o len dessa lista def se as datas da semana estão contidos somente no periodo mensal atual ou se tem mais de um
    bebidas_fat = 0
    for i, mes in enumerate(lista_meses[::-1], start=1):#passando pelo(s) database(s) do mais novo pro mais velho
        if mes <= mes_data:
            if i == 2:#analisando apenas o segundo mes do for
                if mes == '12':
                    ano = str(int(ano)-1)
                    print(f'troquei o ano: {ano}')
            #abrir o data base do periodo mensal da instancia
            wb = op.load_workbook(fr'excell\nw_barbearia_{ano}.xlsx')
            ws = wb[f'{mes}-{ano_abrev}']
            rows = list(ws.values)
            for row in rows:
                #filtrando data
                if row[1] in lista_datas:
                    row = list(row)
                    if '+' in row[7]:
                        row[7]=Soma(row[7].split(' + '))
                    if row[4] != None:
                        bebidas_fat += float(row[7])
                        print(row)
    return bebidas_fat

def Check_datas(data):
    lista_datas = Get_lista_datas_semana()
    if data in lista_datas:
        return True
    else:
        return False


def Update_lista_datas_semana(data, ano):
    def Get_first_week_date(data, ano, weekday_indice):#identificar da data da ultima segunda-feira seja ela no mes ou ano passado
        try:
            data_splited = data.split('-')
            day = int(data_splited[0])
            month = int(data_splited[1])
            year = int(ano)
            if weekday_indice == 0:
                return data
            else:#para o caso de o dia em questão não for segunda
                day = int(day)
                month = int(month)
                for i in range(weekday_indice+1):
                    if day < 1:
                        if month == 1:
                            day = 31
                            month = 12
                            ano = str(int(ano)-1)
                        else:    
                            day = DiasMes(month-1, ano)
                            month -= 1
                    if i == weekday_indice:
                        return [int(ano), month, day]
                    day -= 1
        except:
            print('Erro na subfunção Get_first_week_date da função Update_lista_semanal, arq defs.py.')
    try:
        day, month = data.split('-')
        data_datetime = date(int(ano),int(month),int(day))
        weekday_indice = data_datetime.weekday()
        if weekday_indice != 0:
            year, month, day = Get_first_week_date(data, ano, weekday_indice)
        else:
            day = data_datetime.day
            month = data_datetime.month
            year = data_datetime.year
        #formar a lista de datas desde a ultima segunda feira
        lista_datas = []
        dias_mes = DiasMes(month, ano[2:])
        for i in range(7):#loop que acrescenta as datas da semana na lista
            if day > dias_mes:#condição que recunha a virada do mes
                day = 1
                if month < 12:
                    month += 1
                else:
                    month=1
                    year += 1
            variable_data = Zero_adder(str(day))+'-'+Zero_adder(str(month))
            lista_datas.append(variable_data)
            day += 1
        with open('txts\datas_semana.txt', 'w') as a:
            joined_list=';'.join(lista_datas)
            a.write(joined_list)
            print(f'Lista de datas da semana foram atualizadas: {lista_datas}')
    except:
        print('Erro na função update_datas_semana no arq def.py.')

def Obter_faturamento_semanal_by_barbeiro(data, periodo):
    def Get_meses_lista_datas_semana(lista_datas):
        #formar lista dos meses diferentes separando-os dos dias e tratando-os
        meses = []
        last_mes = ''
        for data in lista_datas:
            data_splited = data.split('-')
            mes = data_splited[1]
            if last_mes != mes:
                meses.append(mes)
            last_mes = mes
        return meses # [atual] | [antigo, atual]
    #try:
    #definições importantes
    data_splited = data.split('-')
    mes_data = data_splited[1]
    periodo_splited = periodo.split('-')
    ano = '20' + periodo_splited[1]
    ano_abrev = periodo_splited[1]
    #obtenção das datas da semana
    if Check_datas(data) == False:#check se as datas da semana são válidas para a data atual
        Update_lista_datas_semana(data, ano)#atualiza as datas da semana
        lista_datas = Get_lista_datas_semana()
    else:
        lista_datas = Get_lista_datas_semana() 
    #calculando o faturamento de cada profissional no(s) periodo(s)
    lista_meses = Get_meses_lista_datas_semana(lista_datas)#o len dessa lista def se as datas da semana estão contidos somente no periodo mensal atual ou se tem mais de um
    profissional1 = profissional2 = profissional3 = profissional4 = 0
    for i, mes in enumerate(lista_meses[::-1], start=1):#passando pelo(s) database(s) do mais novo pro mais velho
        if mes <= mes_data:
            if i == 2:#analisando apenas o segundo mes do for
                if mes == '12':
                    ano = str(int(ano)-1)
                    print(f'troquei o ano: {ano}')
            #abrir o data base do periodo mensal da instancia
            wb = op.load_workbook(fr'excell\nw_barbearia_{ano}.xlsx')
            ws = wb[f'{mes}-{ano_abrev}']
            rows = list(ws.values)
            for row in rows:
                #filtrando data
                if row[1] in lista_datas:
                    row = list(row)
                    if '+' in row[7]:
                        row[7]=Soma(row[7].split(' + '))
                    #filtrando o profissional
                    if row[2] == profissionais[0]:
                        profissional1 += float(row[7])
                    elif row[2] == profissionais[1]:
                        profissional2 += float(row[7])
                    elif row[2] == profissionais[2]:
                        profissional3 += float(row[7])
                    elif row[2] == profissionais[3]:
                        profissional4 += float(row[7])
    return [f'{profissional1:.2f}', f'{profissional2:.2f}', f'{profissional3:.2f}', f'{profissional4:.2f}']

    #print(f'Erro durante a execução da função Obter_faturamento_por_barbeiro_semanal no arquivo {arquivo_name}. lista retornada: [''0.00'', ''0.00'', ''0.00'', ''0.00'']')
    #return ['0.00', '0.00', '0.00', '0.00']

def Box(title):

    root = CTk()
    root.title(title)
    root.geometry('300x150+500+250')
    fonte_c = CTkFont('arial', 25, 'bold')
    
    pb = CTkProgressBar(root, orientation='horizontal', width=275)
    pb.set(0)
    pb.place(relx=0.05, rely=0.9)

    lb = CTkLabel(root, text='Aguarde...', font= fonte_c)
    lb.place(relx=0.3,rely=0.3)


    root.mainloop()

def ProgressBar():
    def Clicker():
        pb.set(pb.get()+0.17)
        lb.configure(text=int(pb.get()*100))

    root = CTk()

    pb = CTkProgressBar(root, orientation='horizontal')
    pb.set(0)
    pb.pack(pady=10)


    bt = CTkButton(root, text='click me', command=lambda:Clicker())
    bt.pack(pady=10)

    lb = CTkLabel(root, text=pb.get())
    lb.pack(pady=10)

    root.mainloop()

Box('Atualizando')