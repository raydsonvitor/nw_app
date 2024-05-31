from tkinter import *
from tkinter.ttk import *
from defs_2_0 import *
from customtkinter import *
import openpyxl as op
from PIL import Image
from check_functions import *
import helper

def On_closing():
    def Etapa():
        etapa_value = 1
        x = pb_tp_ProgressBarBox.get() 
        x +=etapa_value
        pb_tp_ProgressBarBox.set(x)
        if x >= 1:
            lb_tp_ProgressBarBox.configure(text='', image=imagem_success)
            lb_tp_ProgressBarBox.place(relx=0.35,rely=0.2)
        janela_main.update()
    try:
        if check_internet_connection()==True:
            try:
                tp_ProgressBarBox('Salvando...')
                Salvar_no_git()
                Etapa()
                janela_main.destroy()
            except:
                lb_tp_ProgressBarBox.configure(text='  Erro ao salvar!', image=imagem_fail, font=fonte, compound='left')
                lb_tp_ProgressBarBox.place(relx=0.1,rely=0.2)
                janela_main.update()
                sleep(1.5)
                janela_main.destroy()
        else:
            print('Sem conexão com a internet. Fechando sem salvar arquivos na nuvem.')
    except:
        print('Erro na função On_closing, arquivo app.py.')
        

janela_main = CTk()
janela_main.iconbitmap(r'images\icone.ico')
barradetarefas_height = 70
tela_width = janela_main.winfo_screenwidth() - 15
tela_height = janela_main.winfo_screenheight() - barradetarefas_height
janela_main.geometry(f'{tela_width}x{tela_height}+0+0')
janela_main.title('Night Wolf ADM')
janela_main.resizable(False, False)
janela_main.protocol("WM_DELETE_WINDOW", On_closing)


if check_datatime_before_run_app() == False:
    x = Show_fail_msgbox(janela_main, 'Data do computador está errada. O programa não poderá ser inicializado')
    exit()

#definicoes primordiais:
#cor das figuras dos botoes: #004aad
set_appearance_mode('dark')
set_default_color_theme('dark-blue')
fonte_sinalizer = CTkFont('arial', 10, 'bold')
fonte = CTkFont('arial', 15)
fonte_b = CTkFont('arial', 15, 'bold')
fonte_c = CTkFont('arial', 25, 'bold')
profissionais = ['VITOR', 'KAUAN', 'FREE1','FREE2']
despesas = ['CONSUMÍVEIS', 'ALUGUEL', 'ÁGUA', 'LUZ', 'INTERNET','FUNDOS', 'ESTORNO', 'OUTRO']
form_pgmt_entrada = ['DINHEIRO', 'PIX QR', 'DÉBITO', 'CRÉDITO','PIX CHAVE','MENSAL']
form_pgmt_saida = ['DINHEIRO', 'BANCO', 'CARTÃO']
form_pgmt_cartao = ['DÉBITO', 'CRÉDITO']
colunas_database = ('id' ,'data', 'profissional' ,'serviços/descrição', 'bebidas', 'produtos' ,'form pgmt' ,'entrada' ,'saída', 'hora')
periodo = '10-24'
data = GetData()
ano = '20'+periodo[3:]
meiospgmt=1
wb = op.load_workbook(rf'excell\nw_barbearia_{ano}.xlsx')
sinalizer_check = False
imagem_success = CTkImage(light_image=Image.open(r'images\success.png'), size=(80,80))
imagem_fail = CTkImage(light_image=Image.open(r'images\fail.png'), size=(80,80))

#print info de inicialialzação
Lin()
print('Dados de inicialização\n')
print(f'data definida: {data}')
print(f'Periodo definido: {periodo}')
print('versao: 2.0')
Lin()

#Funções

def Refresh_Widgets(arg):
    try:
        if arg==1:#Registrar Entrada Frame wgs
            profissional_var.set('')
            tb_0_fm_0_wg_4_var.set('')
            tb_0_fm_0_wg_12_var.set('')
            tb_0_fm_0_wg_15_var.set('')
            tb_0_fm_0_wg_7.set('MODO DE PGMT. 1')
            tb_0_fm_0_wg_9.delete(0, 'end')
            tb_0_fm_0_twg_1.set('MODO DE PGMT. 2')
            tb_0_fm_0_twg_2.delete(0, 'end')
        elif arg==2:
            tb_1_fm_0_wg_2.set('SELECIONAR DESPESA')
            tb_1_fm_0_wg_4.set('MODO DE PGMT')
            tb_1_fm_0_wg_5.delete(0, 'end')
        elif arg ==3:
            sinalizer.place_forget()
            sinalizer_0.place_forget()
            sinalizer_1.place_forget()
            sinalizer_2.place_forget()
            sinalizer_3.place_forget()
            sinalizer_4.place_forget()
            sinalizer_5.place_forget()
            sinalizer_6.place_forget()
    except:
        print('Erro na função Refresh_Widgets arq app.py')

def RegistrarEntrada(wb):
    def Etapa():
        etapa_value = 0.34
        x = pb_tp_ProgressBarBox.get() 
        x +=etapa_value
        pb_tp_ProgressBarBox.set(x)
        if x >= 1:
            lb_tp_ProgressBarBox.configure(text='', image=imagem_success)
            lb_tp_ProgressBarBox.place(relx=0.35,rely=0.2)
        janela_main.update()

    tp_ProgressBarBox('Registrando...')
    try:
        Refresh_Widgets(3)
        #id
        lastid = GetLastId(wb, periodo, colunas_database)
        id = int(lastid)+1
        #profissional
        profissional = profissional_var.get()
        #serviços
        servicos = tb_0_fm_0_wg_4_var.get()
        #bebidas
        bebidas = tb_0_fm_0_wg_12_var.get()
        #produtos
        produtos = tb_0_fm_0_wg_15_var.get()
        #form pgmt
        if meiospgmt==1:
            meiopgmt = tb_0_fm_0_wg_7.get()
            entrada = tb_0_fm_0_wg_9.get().strip().replace(',','.')
        else:
            #meiopgmt 1
            meiopgmt = tb_0_fm_0_wg_7.get()
            entrada = tb_0_fm_0_wg_9.get().strip().replace(',','.')
            #meiopmtg 2
            meiopgmt2=tb_0_fm_0_twg_1.get()
            entrada2 = tb_0_fm_0_twg_2.get().strip().replace(',','.')
            
            meiopgmt = f'{meiopgmt} + {meiopgmt2}'
            entrada = f'{entrada} + {entrada2}'
        #hora
        hora = GetHora()
        Etapa()
        #checkar os dados obtidos
        check = Check_entrada(profissional, meiopgmt, entrada, servicos, bebidas, produtos)
        Etapa()
        if check == True:
            print('row aprovada para entrar no database:\n')
            row = [id, data, profissional, servicos, bebidas, produtos, meiopgmt, entrada,  '',hora]
            #get row into dt
            ws = wb[periodo]
            ws.append(row)
            wb.save(rf'excell\nw_barbearia_{ano}.xlsx')
            print(f'Row salva com o ID: {id}')
            #get row into tv
            tv.insert('', index= 'end', values=row)
            #refresh widgets
            Refresh_Widgets(1)
            Etapa()
            sleep(0.5)
            top.destroy()
        else:
            print('row desaprovada para entrar no database')
            print(check[1])
            #sinalizar qual widget ficou errado
            if 'meiopgmt1' in check[1]:
                sinalizer_0.place(relx=0.20, rely=0.450)
            if 'meiopgmt2' in check[1]:
                sinalizer_1.place(relx=0.55, rely=0.450)
            if 'valor1' in check[1]:
                sinalizer_2.place(relx=0.28, rely=0.530)
            if 'valor2' in check[1]:
                sinalizer_3.place(relx=0.63, rely=0.530)
            if 'profissional' in check[1]:
                sinalizer.place(relx=0.45, rely=0.15)
            top.destroy()
    except:
        print('Erro na função RegistrarEntrada, arquivo app.py')
        lb_tp_ProgressBarBox.configure(text='  Erro ao registrar!', image=imagem_fail, font=fonte, compound='left')
        lb_tp_ProgressBarBox.place(relx=0.1,rely=0.2)
        janela_main.update()
        sleep(1.5)
        top.destroy()

def RegistrarSaida():
    def Etapa():
        etapa_value = 0.34
        x = pb_tp_ProgressBarBox.get() 
        x +=etapa_value
        pb_tp_ProgressBarBox.set(x)
        if x >= 1:
            lb_tp_ProgressBarBox.configure(text='', image=imagem_success)
            lb_tp_ProgressBarBox.place(relx=0.35,rely=0.2)
        janela_main.update()

    tp_ProgressBarBox('Registrando...')
    try:
        Refresh_Widgets(3)
        ##obter dados dos wg para a row
        #id
        lastid = GetLastId(wb, periodo, colunas_database)
        id = int(lastid)+1
        #despesa
        despesa = tb_1_fm_0_wg_2.get().replace('SELECIONAR DESPESA', '')
        #meiopgmt
        meiopgmt = tb_1_fm_0_wg_4.get().replace('MODO DESPESA', '')
        #saida \ valor
        saida = tb_1_fm_0_wg_5.get().strip().replace(',','.')
        #hora
        hora = GetHora()
        Etapa()
        #checkar dados obtidos
        check = Check_saida(despesa, meiopgmt, saida)
        Etapa()
        if check == True:
            print('row aprovada para entrar no database')
            row = [id, data, '', despesa, '', '', meiopgmt, '', saida, hora]
            #get row into dt
            ws = wb[periodo]
            ws.append(row)
            wb.save(rf'excell\nw_barbearia_{ano}.xlsx')
            print(f'Row salva com o ID: {id}')
            #get row into tv
            tv.insert('', index= 'end', values=row)
            #refresh widgets
            Refresh_Widgets(2)
            #show check
            Etapa()
            sleep(0.5)
            top.destroy()

        else:
            print('row desaprovada para entrar no database')
            if 'despesa' in check[1]:
                sinalizer_4.place(relx=0.05, rely=0.15)
            if 'meiopgmt' in check[1]:
                sinalizer_5.place(relx=0.05, rely=0.3)
            if 'valor' in check[1]:
                sinalizer_6.place(relx=0.60, rely=0.3)
            top.destroy()
    except:
        print('Erro na função RegistrarSaida, arquivo app.py. Nenhum valor retornado')
        lb_tp_ProgressBarBox.configure(text='  Erro ao registrar!', image=imagem_fail, font=fonte, compound='left')
        lb_tp_ProgressBarBox.place(relx=0.1,rely=0.2)
        janela_main.update()
        sleep(1.5)
        top.destroy()

def LoadData():
    try:
        ano = '20'+periodo[3:]
        ws = wb[periodo]
        list_values = list(ws.values)
        if list_values != [colunas_database]:
            for row in list_values[1:]:
                if list(row)[1]==data:
                    row = List_change_nothing_to_something(list(row) ,'-')
                    tv.insert('', END,values=row)
            print(f'Load do arquvio nw_barbearia_{ano}.xlsx(sheet: {periodo}, data:{data}) para a Treewview realizado')
        else:
            print('Sheet vazia. Nada foi loadado na Treeview.')
    except:
        print('Erro ao dar o Load dos dados na treeview')

def Atualizar():
    def Etapa():
        etapa_value = 0.17
        x = pb_tp_ProgressBarBox.get() 
        x +=etapa_value
        pb_tp_ProgressBarBox.set(x)
        if x >= 1:
            lb_tp_ProgressBarBox.configure(text='', image=imagem_success)
            lb_tp_ProgressBarBox.place(relx=0.35,rely=0.2)
        janela_main.update()

    tp_ProgressBarBox('Atualizando...')
    #try:
    faturamento_por_barbeiro_diario = Obter_faturamento_diario_by_barbeiro(wb, data, periodo)
    tot_diario = helper.format_to_moeda(helper.format_to_float(faturamento_por_barbeiro_diario[0])+helper.format_to_float(faturamento_por_barbeiro_diario[1])+helper.format_to_float(faturamento_por_barbeiro_diario[2])+helper.format_to_float(faturamento_por_barbeiro_diario[3]))
    label_1_textvar.set(f'R${faturamento_por_barbeiro_diario[0]}')
    label_3_textvar.set(f'R${faturamento_por_barbeiro_diario[1]}')
    label_5_textvar.set(f'R${faturamento_por_barbeiro_diario[2]}')
    label_7_textvar.set(f'R${faturamento_por_barbeiro_diario[3]}')
    label_9_textvar.set(f'R${tot_diario}')
    Etapa()
    faturamento_por_barbeiro_semanal = Obter_faturamento_semanal_by_barbeiro(data, periodo)
    print(faturamento_por_barbeiro_semanal)
    tot_semanal = helper.format_to_moeda(helper.format_to_float(faturamento_por_barbeiro_semanal[0])+helper.format_to_float(faturamento_por_barbeiro_semanal[1])+helper.format_to_float(faturamento_por_barbeiro_semanal[2])+helper.format_to_float(faturamento_por_barbeiro_semanal[3]))
    Frame_5_Widget_2_textvar.set(f'R${faturamento_por_barbeiro_semanal[0]}')
    Frame_5_Widget_4_textvar.set(f'R${faturamento_por_barbeiro_semanal[1]}')
    Frame_5_Widget_6_textvar.set(f'R${faturamento_por_barbeiro_semanal[2]}')
    Frame_5_Widget_8_textvar.set(f'R${faturamento_por_barbeiro_semanal[3]}')
    Frame_5_Widget_10_textvar.set(f'R${tot_semanal}')
    Etapa()
    faturamento_por_barbeiro_mensal = Obter_faturamento_mensal_by_barbeiro(wb, periodo)
    tot_mensal = helper.format_to_moeda(helper.format_to_float(faturamento_por_barbeiro_mensal[0])+helper.format_to_float(faturamento_por_barbeiro_mensal[1])+helper.format_to_float(faturamento_por_barbeiro_mensal[2])+helper.format_to_float(faturamento_por_barbeiro_mensal[3]))
    Frame_6_Widget_2_textvar.set(f'R${faturamento_por_barbeiro_mensal[0]}')
    Frame_6_Widget_4_textvar.set(f'R${faturamento_por_barbeiro_mensal[1]}')
    Frame_6_Widget_6_textvar.set(f'R${faturamento_por_barbeiro_mensal[2]}')
    Frame_6_Widget_8_textvar.set(f'R${faturamento_por_barbeiro_mensal[3]}')
    Frame_6_Widget_10_textvar.set(f'R${tot_mensal}')
    Etapa()
    faturamento_dia_by_formpgmt = Get_faturamento_dia_by_formpgmt(wb, periodo, data) # [dinheiro, cartão, pix]
    caixa = Obter_caixa(data, periodo)
    frame_7_Widget_1_textvar.set(f'R${faturamento_dia_by_formpgmt[0]}')
    frame_7_Widget_3_textvar.set(f'R${faturamento_dia_by_formpgmt[1]}')
    frame_7_Widget_5_textvar.set(f'R${faturamento_dia_by_formpgmt[2]}')
    frame_7_Widget_12_textvar.set(f'R${faturamento_dia_by_formpgmt[3]}')
    frame_7_Widget_8_textvar.set(f'R${caixa}')
    atendimentos_var.set(faturamento_por_barbeiro_diario[4])
    Etapa()
    print('Widgets atualizados!')
    DeleteTreeviewData()
    LoadData()
    Etapa()
    internet_connected = check_internet_connection()
    if internet_connected:
        frame_0_widgets_5.configure(image=imagem_internet_on) 
    else:
        frame_0_widgets_5.configure(image=imagem_internet_off)
    Etapa()
    sleep(0.5)
    top.destroy()
    #except:
    #    print('Erro na função Atualizar, arquivo app.py')
    #    lb_tp_ProgressBarBox.configure(text='  Erro ao atualizar!', image=imagem_fail, font=fonte, compound='left')
    #    lb_tp_ProgressBarBox.place(relx=0.1,rely=0.2)
    #    janela_main.update()
    #    sleep(1.5)
    #    top.destroy()


def FecharCaixa(caixa_restante):
    def Etapa():
        etapa_value = 0.5
        x = pb_tp_ProgressBarBox.get() 
        x +=etapa_value
        pb_tp_ProgressBarBox.set(x)
        if x >= 1:
            lb_tp_ProgressBarBox.configure(text='', image=imagem_success)
            lb_tp_ProgressBarBox.place(relx=0.35,rely=0.2)
        janela_main.update()
    tp_ProgressBarBox('Fechando caixa...')
    try:
        if caixa_restante!='':
            #reescrevendo o arquivo
            with open(r'txts\caixa.txt', 'w') as a:
                a.write(caixa_restante)
                print(f'Saldo do caixa atualizado: {caixa_restante}')
            Etapa()
            #limpando widget
            frame_7_Widget_10.delete(0, 'end')
            Etapa()
            sleep(0.5)
            top.destroy()
        else:
            lb_tp_ProgressBarBox.configure(text='Valor não digitado.')
            lb_tp_ProgressBarBox.place(relx=0.15,rely=0.2)
            janela_main.update()
            sleep(1)
            top.destroy()

    except:
        print('Erro na função FecharCaixa no arquivo app_barbearia.py')
        lb_tp_ProgressBarBox.configure(text='  Erro ao fechar o caixa!', image=imagem_fail, font=fonte, compound='left')
        lb_tp_ProgressBarBox.place(relx=0.1,rely=0.2)
        janela_main.update()
        sleep(1.5)
        top.destroy()

def DeleteTreeviewData():
    try:
        for i in tv.get_children():
            tv.delete(i)        
    except:
        print('Erro na função DeleteTreeviewDados, arquivo app.py')

def DeleteTreeviewItem():
    def Etapa():
        etapa_value = 0.5
        x = pb_tp_ProgressBarBox.get() 
        x +=etapa_value
        pb_tp_ProgressBarBox.set(x)
        if x >= 1:
            lb_tp_ProgressBarBox.configure(text='', image=imagem_success)
            lb_tp_ProgressBarBox.place(relx=0.35,rely=0.2)
            janela_main.update()
        janela_main.update()
    try:
        #pegando a row da treeview
        try:
            item= tv.selection()[0]
        except:
            print('Nenhum item selecionado!')
            return 
        tl_spv_password_request(janela_main, tela_width, tela_height, fonte_b)
        global resultado_senha
        if resultado_senha:
            tp_ProgressBarBox('Excluindo...')
            valores=tv.item(item, 'values')
            print(valores)
            tv.delete(item)
            id=valores[0]
            print(f'linha de código {id} deletado na treeview')
            Etapa()
            #abrindo o database
            ws=wb[periodo]
            rows=list(ws.values)[1:]
            index = 2
            for row in rows:
                if str(row[0]) == str(id):
                    #check = Get_password_operator()
                    #if check == True:
                    ws.delete_rows(index, 1)
                    wb.save(rf'excell\nw_barbearia_{ano}.xlsx')    
                    print(f'linha de código {id} e index {index} deletado na database')
                    break
                index+=1
            Etapa()
            sleep(0.5)
            top.destroy()
        else:
            print('Senha inválida')
    except:
        print('Erro na função DeleteTreeviewItem, arquivo app.py')
        lb_tp_ProgressBarBox.configure(text='  Erro ao deletar!', image=imagem_fail, font=fonte, compound='left')
        lb_tp_ProgressBarBox.place(relx=0.1,rely=0.2)
        janela_main.update()
        sleep(1.5)
        top.destroy()

def tl_spv_password_request(janela, tela_width, tela_height, font):
    resultado_senha = None
    def Check():
        global resultado_senha
        if entry.get() == '3006':
            toplevel.destroy()
            print('retornando True')
            resultado_senha = True 
        else:
            entry.delete(0, END)
            label_sinalizer = CTkLabel(toplevel, text='senha inválida!', text_color='red', height=10)
            label_sinalizer.place(relx=0.36, rely=0.36)
            resultado_senha = False

    toplevel = CTkToplevel(janela)
    toplevel.attributes('-topmost', 'true')
    toplevel.title('Insirir senha de supervisor')
    toplevel_width = 300
    toplevel_height = 100
    toplevel.geometry(f'{toplevel_width}x{toplevel_height}+{tela_width//2-toplevel_width//2}+{tela_height//2-toplevel_height//2}')
    toplevel.resizable(False, False)
    label = CTkLabel(toplevel, text='senha:', font=font)
    label.grid(row=0, column=0, pady=(10, 5), padx=5)
    entry = CTkEntry(toplevel, width= 200, height=15, font=font, show='*')
    entry.focus_set()
    entry.grid(row=0, column=1, pady=(10, 5), sticky='WE')
    button = CTkButton(toplevel, text='ENTER', font=font, command=lambda:Check())
    button.grid(row=1, column=1, columnspan=1, pady=15)
    toplevel.bind('<Return>', lambda event: Check())

    janela.wait_window(toplevel)


def tl_0():
    def ok():
        lista = get_servicos_var_values()
        global lista_tl_0_servicos
        lista_tl_0_servicos = lista
        Get_lista_servicos_into_wg(lista_tl_0_servicos)
        tl_0.destroy()

    def get_servicos_var_values():
        lista=[]
        lista.append(tl_0_wg_2_var.get())
        lista.append(tl_0_wg_3_var.get())
        lista.append(tl_0_wg_4_var.get())    
        lista.append(tl_0_wg_5_var.get())
        lista.append(tl_0_wg_6_var.get())
        lista.append(tl_0_wg_7_var.get())
        lista.append(tl_0_wg_9_var.get())
        lista.append(tl_0_wg_10_var.get())
        lista.append(tl_0_wg_11_var.get())
        return lista

    def Get_lista_servicos_into_wg(lista):
        lista1 = []
        for item in lista:
            if item != '':
                lista1.append(item)
        lista_string = ' + '.join(lista1)
        tb_0_fm_0_wg_4_var.set(lista_string)

    #definições
    tl_width = 1000
    tl_height = 600
    tl_0 = CTkToplevel(janela_main, fg_color='WHITE')
    tl_0.geometry(f'{tl_width}x{tl_height}+200+50')
    tl_0.resizable(False,False)
    tl_0.attributes('-topmost', 'true')

    #Var's (9)
    tl_0_wg_2_var=StringVar(value='')
    tl_0_wg_3_var=StringVar(value='')
    tl_0_wg_4_var=StringVar(value='')
    tl_0_wg_5_var=StringVar(value='')
    tl_0_wg_6_var=StringVar(value='')
    tl_0_wg_7_var=StringVar(value='')
    tl_0_wg_9_var=StringVar(value='')
    tl_0_wg_10_var=StringVar(value='')
    tl_0_wg_11_var=StringVar(value='')

    #titlo wg
    tl_0_wg_0 = CTkLabel(tl_0, fg_color='blue', bg_color='blue',text='SELECIONE OS SERVIÇOS PRESTADOS:', width= tl_width, height=30, font=fonte_b, text_color='white')
    tl_0_wg_0.place(x=0, y=0)

    #subtilo wg
    tl_0_wg_1 = CTkLabel(tl_0, text='SERVIÇOS BÁSICOS:', font=fonte_b, text_color='black')
    tl_0_wg_1.place(relx=0.05, rely=0.08)

    #checkboxers servicos basicos wdgs    
    tl_0_wg_2 = CTkCheckBox(tl_0, variable=tl_0_wg_2_var,checkbox_height=100, checkbox_width=100, text='Corte', font=fonte_c, text_color='black', onvalue='CORTE', offvalue='')
    tl_0_wg_2.place(relx=0.05, rely=0.15)
    tl_0_wg_3 = CTkCheckBox(tl_0, variable=tl_0_wg_3_var,checkbox_height=100, checkbox_width=100, text='Sobrancelha', font=fonte_c, text_color='black', onvalue='SOBRANCELHA', offvalue='')
    tl_0_wg_3.place(relx=0.40, rely=0.15)
    tl_0_wg_4 = CTkCheckBox(tl_0, variable=tl_0_wg_4_var,checkbox_height=100, checkbox_width=100, text='Barba', font=fonte_c, text_color='black', onvalue='BARBA', offvalue='')
    tl_0_wg_4.place(relx=0.75, rely=0.15)
    tl_0_wg_5 = CTkCheckBox(tl_0, variable=tl_0_wg_5_var,checkbox_height=100, checkbox_width=100, text='Bigode', font=fonte_c, text_color='black', onvalue='BIGODE', offvalue='')
    tl_0_wg_5.place(relx=0.05, rely=0.35)
    tl_0_wg_6 = CTkCheckBox(tl_0, variable=tl_0_wg_6_var,checkbox_height=100, checkbox_width=100, text='Contorno', font=fonte_c, text_color='black', onvalue='CONTORNO', offvalue='')
    tl_0_wg_6.place(relx=0.40, rely=0.35)
    tl_0_wg_7 = CTkCheckBox(tl_0, variable=tl_0_wg_7_var,checkbox_height=100, checkbox_width=100, text='Raspagem', font=fonte_c, text_color='black', onvalue='RASPAGEM', offvalue='')
    tl_0_wg_7.place(relx=0.75, rely=0.35)

    #subtilo wg
    tl_0_wg_8 = CTkLabel(tl_0, text='SERVIÇOS COM QUÍMICA:', font=fonte_b, text_color='black')
    tl_0_wg_8.place(relx=0.05, rely=0.60)

    #checkboxers servicos basicos wdgs
    tl_0_wg_9 = CTkCheckBox(tl_0, variable=tl_0_wg_9_var,checkbox_height=100, checkbox_width=100, text='Pigmentação', font=fonte_c, text_color='black', onvalue='PIGMENTAÇÃO', offvalue='')
    tl_0_wg_9.place(relx=0.05, rely=0.67)
    tl_0_wg_10 = CTkCheckBox(tl_0, variable=tl_0_wg_10_var,checkbox_height=100, checkbox_width=100, text='Luzes', font=fonte_c, text_color='black', onvalue='LUZES', offvalue='')
    tl_0_wg_10.place(relx=0.40, rely=0.67)
    tl_0_wg_11 = CTkCheckBox(tl_0, variable=tl_0_wg_11_var,checkbox_height=100, checkbox_width=100, text='Platinado', font=fonte_c, text_color='black', onvalue='PLATINADO', offvalue='')
    tl_0_wg_11.place(relx=0.75, rely=0.67)

    #botoes wdgs
    tl_0_wg_12 = CTkButton(tl_0, state='normal',text='OK', font= fonte_b, command=lambda:ok())
    tl_0_wg_12.place(relx=0.40, rely=0.9)

def tl_1():
    def ok():
        lista = get_bebidas_var_values()
        global lista_tl_1_bebidas
        lista_tl_1_bebidas = lista#ele atualiza a lista que ta no root
        Get_lista_bebidas_into_wg(lista_tl_1_bebidas)
        tl_1.destroy()

    def click(wg, onvalue):
        if wg.get()=='':   #se o checkbox estiver desligado ele ira ativar 
            wg.set(onvalue)
        else:#se estiver ligado ele desativa
            wg.set('')

    def Get_lista_bebidas_into_wg(lista):
        lista1 = []
        for item in lista:
            if item != '':
                lista1.append(item)
        lista_string = ' + '.join(lista1)
        tb_0_fm_0_wg_12_var.set(lista_string)

    def get_bebidas_var_values():
        lista=[]
        if tl_1_wg_3_var.get()!='':
            lista.append(f'{tl_1_wg_3_0_var.get()} {tl_1_wg_3_var.get()}')
        if tl_1_wg_5_var.get()!='':
            lista.append(f'{tl_1_wg_5_0_var.get()} {tl_1_wg_5_var.get()}')
        if tl_1_wg_7_var.get()!='':
            lista.append(f'{tl_1_wg_7_0_var.get()} {tl_1_wg_7_var.get()}')  
        if tl_1_wg_10_var.get()!='':
            lista.append(f'{tl_1_wg_10_0_var.get()} {tl_1_wg_10_var.get()}')  
        if tl_1_wg_12_var.get()!='':
            lista.append(f'{tl_1_wg_12_0_var.get()} {tl_1_wg_12_var.get()}')  
        if tl_1_wg_14_var.get()!='':
            lista.append(f'{tl_1_wg_14_0_var.get()} {tl_1_wg_14_var.get()}')  
        if tl_1_wg_16_var.get()!='':
            lista.append(f'{tl_1_wg_16_0_var.get()} {tl_1_wg_16_var.get()}')  
        if tl_1_wg_19_var.get()!='':
            lista.append(f'{tl_1_wg_19_0_var.get()} {tl_1_wg_19_var.get()}')  
        if tl_1_wg_21_var.get()!='':
            lista.append(f'{tl_1_wg_21_0_var.get()} {tl_1_wg_21_var.get()}')
        return lista

    #definições
    tl_width = 1000
    tl_height = 675
    tl_1 = CTkToplevel(janela_main, fg_color='WHITE')
    tl_1.geometry(f'{tl_width}x{tl_height}+200+0')
    tl_1.resizable(False,False)
    tl_1.title('SELECIONAR BEBIDAS')
    tl_1.attributes('-topmost', 'true')

    #titlo wg
    tl_1_wg_0 = CTkLabel(tl_1, fg_color='blue', bg_color='blue',text='SELECIONE AS BEBIDAS VENDIDAS:', width= tl_width, height=30, font=fonte_b, text_color='white')
    tl_1_wg_0.place(x=0, y=0)

    #subtitlos
    tl_1_wg_1 = CTkLabel(tl_1, text='CERVEJAS:', font=fonte_b, text_color='black')
    tl_1_wg_1.place(relx=0.05, rely=0.05)

    #Var's
    tl_1_wg_3_var = StringVar()
    tl_1_wg_5_var = StringVar()
    tl_1_wg_7_var = StringVar()
    tl_1_wg_10_var = StringVar()
    tl_1_wg_12_var = StringVar()
    tl_1_wg_14_var = StringVar()
    tl_1_wg_16_var = StringVar()
    tl_1_wg_19_var = StringVar()
    tl_1_wg_21_var = StringVar()
    
    tl_1_wg_3_0_var = IntVar()
    tl_1_wg_5_0_var = IntVar()
    tl_1_wg_7_0_var = IntVar()
    tl_1_wg_10_0_var = IntVar()
    tl_1_wg_12_0_var = IntVar()
    tl_1_wg_14_0_var = IntVar()
    tl_1_wg_16_0_var = IntVar()
    tl_1_wg_19_0_var = IntVar()
    tl_1_wg_21_0_var = IntVar()

    #wgs cervejas
    img_schin_latao = CTkImage(light_image=Image.open(r'images\schin_latao.png'), size=(75, 75))
    tl_1_wg_2 = CTkButton(tl_1, image=img_schin_latao, text='', hover=True, fg_color='white', command=lambda:click(tl_1_wg_3_var, 'SCHIN LATÃO'))
    tl_1_wg_2.place(relx=0.05, rely=0.10)
    tl_1_wg_3 = CTkCheckBox(tl_1, variable=tl_1_wg_3_var, text='Schin latão', font=fonte_c, text_color='black', onvalue='SCHIN LATÃO', offvalue='')
    tl_1_wg_3.place(relx=0.05, rely=0.24)
    tl_1_wg_3_0 = Spinbox(tl_1, from_=1, to=99, font='Helvetica', width=3, bg='lightblue', textvariable=tl_1_wg_3_0_var)
    tl_1_wg_3_0.place(relx=0.20, rely=0.17)

    img_polar_latao = CTkImage(light_image=Image.open(r'images\polar_latao.png'), size=(75, 75))
    tl_1_wg_4 = CTkButton(tl_1, image=img_polar_latao, text='', hover=True, fg_color='white', command=lambda:click(tl_1_wg_5_var, 'POLAR LATÃO'))
    tl_1_wg_4.place(relx=0.30, rely=0.10)
    tl_1_wg_5 = CTkCheckBox(tl_1, variable=tl_1_wg_5_var, text='Polar latão', font=fonte_c, text_color='black', onvalue='POLAR LATÃO', offvalue='')
    tl_1_wg_5.place(relx=0.30, rely=0.24)
    tl_1_wg_5_0 = Spinbox(tl_1, from_=1, to=99, font='Helvetica', width=3, bg='lightblue', textvariable=tl_1_wg_5_0_var)
    tl_1_wg_5_0.place(relx=0.45, rely=0.17)

    img_bud_latao = CTkImage(light_image=Image.open(r'images\bud_latao.png'), size=(75, 75))
    tl_1_wg_6 = CTkButton(tl_1, image=img_bud_latao, text='', hover=True, fg_color='white', command=lambda:click(tl_1_wg_7_var, 'BUD LATÃO'))
    tl_1_wg_6.place(relx=0.55, rely=0.10)
    tl_1_wg_7 = CTkCheckBox(tl_1, variable=tl_1_wg_7_var, text='Bud latão', font=fonte_c, text_color='black', onvalue='BUD LATÃO', offvalue='')
    tl_1_wg_7.place(relx=0.55, rely=0.24)
    tl_1_wg_7_0 = Spinbox(tl_1, from_=1, to=99, font='Helvetica', width=3, bg='lightblue', textvariable=tl_1_wg_7_0_var)
    tl_1_wg_7_0.place(relx=0.70, rely=0.17)

    #subtitlos
    tl_1_wg_8 = CTkLabel(tl_1, text='BEBIDAS SEM ÁLCOOL:', font=fonte_b, text_color='black')
    tl_1_wg_8.place(relx=0.05, rely=0.33)

    #wgs latas e garrafas
    img_schin_latao = CTkImage(light_image=Image.open(r'images\coca_lata.png'), size=(75, 75))
    tl_1_wg_9 = CTkButton(tl_1, image=img_schin_latao, text='', hover=True, fg_color='white', command=lambda:click(tl_1_wg_10_var, 'COCA LATA'))
    tl_1_wg_9.place(relx=0.05, rely=0.38)
    tl_1_wg_10 = CTkCheckBox(tl_1, variable=tl_1_wg_10_var, text='Coca lata', font=fonte_c, text_color='black', onvalue='COCA LATA', offvalue='')
    tl_1_wg_10.place(relx=0.05, rely=0.52)#abaixo da imagem
    tl_1_wg_10_0 = Spinbox(tl_1, from_=1, to=99, font='Helvetica', width=3, bg='lightblue', textvariable=tl_1_wg_10_0_var)
    tl_1_wg_10_0.place(relx=0.20, rely=0.45)

    img_polar_latao = CTkImage(light_image=Image.open(r'images\guarana_lata.png'), size=(75, 75))
    tl_1_wg_11 = CTkButton(tl_1, image=img_polar_latao, text='', hover=True, fg_color='white', command=lambda:click(tl_1_wg_12_var, 'GUARANÁ LATA'))
    tl_1_wg_11.place(relx=0.30, rely=0.38)
    tl_1_wg_12 = CTkCheckBox(tl_1, variable=tl_1_wg_12_var, text='Coca lata', font=fonte_c, text_color='black', onvalue='GUARANÁ LATA', offvalue='')
    tl_1_wg_12.place(relx=0.30, rely=0.52)#abaixo da imagem
    tl_1_wg_12_0 = Spinbox(tl_1, from_=1, to=99, font='Helvetica', width=3, bg='lightblue', textvariable=tl_1_wg_12_0_var)
    tl_1_wg_12_0.place(relx=0.45, rely=0.45)

    img_bud_latao = CTkImage(light_image=Image.open(r'images\monster.png'), size=(75, 75))
    tl_1_wg_13 = CTkButton(tl_1, image=img_bud_latao, text='', hover=True, fg_color='white', command=lambda:click(tl_1_wg_14_var, 'MONSTER'))
    tl_1_wg_13.place(relx=0.55, rely=0.38)
    tl_1_wg_14 = CTkCheckBox(tl_1, variable=tl_1_wg_14_var, text='Monster', font=fonte_c, text_color='black', onvalue='MONSTER', offvalue='')
    tl_1_wg_14.place(relx=0.55, rely=0.52)#abaixo da imagem
    tl_1_wg_14_0 = Spinbox(tl_1, from_=1, to=99, font='Helvetica', width=3, bg='lightblue', textvariable=tl_1_wg_14_0_var)
    tl_1_wg_14_0.place(relx=0.70, rely=0.45)

    img_bud_latao = CTkImage(light_image=Image.open(r'images\agua.png'), size=(105, 75))
    tl_1_wg_15 = CTkButton(tl_1, image=img_bud_latao, text='', hover=True, fg_color='white', command=lambda:click(tl_1_wg_16_var, 'ÁGUA'))
    tl_1_wg_15.place(relx=0.80, rely=0.38)
    tl_1_wg_16 = CTkCheckBox(tl_1, variable=tl_1_wg_16_var, text='Água 500ml', font=fonte_c, text_color='black', onvalue='ÁGUA', offvalue='')
    tl_1_wg_16.place(relx=0.80, rely=0.52)#abaixo da imagem
    tl_1_wg_16_0 = Spinbox(tl_1, from_=1, to=99, font='Helvetica', width=3, bg='lightblue', textvariable=tl_1_wg_16_0_var)
    tl_1_wg_16_0.place(relx=0.95, rely=0.45)

    #subtitlos
    tl_1_wg_17 = CTkLabel(tl_1, text='COPÕES:', font=fonte_b, text_color='black')
    tl_1_wg_17.place(relx=0.05, rely=0.61)

    #wgs copao
    img_schin_latao = CTkImage(light_image=Image.open(r'images\copao.png'), size=(75, 105))
    tl_1_wg_18 = CTkButton(tl_1, image=img_schin_latao, text='', hover=True, fg_color='white', command=lambda:click(tl_1_wg_19_var, 'COPÃO COMUM'))
    tl_1_wg_18.place(relx=0.05, rely=0.65)
    tl_1_wg_19 = CTkCheckBox(tl_1, variable=tl_1_wg_19_var, text='Copão Comun', font=fonte_c, text_color='black', onvalue='COPÃO COMUM', offvalue='')
    tl_1_wg_19.place(relx=0.05, rely=0.83)#abaixo da imagem
    tl_1_wg_19_0 = Spinbox(tl_1, from_=1, to=99, font='Helvetica', width=3, bg='lightblue', textvariable=tl_1_wg_19_0_var)
    tl_1_wg_19_0.place(relx=0.20, rely=0.72)

    img_polar_latao = CTkImage(light_image=Image.open(r'images\copao.png'), size=(75, 105))
    tl_1_wg_20 = CTkButton(tl_1, image=img_polar_latao, text='', hover=True, fg_color='white', command=lambda:click(tl_1_wg_21_var, 'COPÃO RED'))
    tl_1_wg_20.place(relx=0.30, rely=0.65)
    tl_1_wg_21 = CTkCheckBox(tl_1, variable=tl_1_wg_21_var, text='Copão Red', font=fonte_c, text_color='black', onvalue='COPÃO RED', offvalue='')
    tl_1_wg_21.place(relx=0.30, rely=0.83)#abaixo da imagem
    tl_1_wg_21_0 = Spinbox(tl_1, from_=1, to=99, font='Helvetica', width=3, bg='lightblue', textvariable=tl_1_wg_21_0_var)
    tl_1_wg_21_0.place(relx=0.45, rely=0.72)

    #botoes wdgs
    tl_0_wg_22 = CTkButton(tl_1, state='normal',text='OK', font= fonte_b, command=lambda:ok())
    tl_0_wg_22.place(relx=0.40, rely=0.93)

def tl_2():
    def ok():
        lista = Get_values()
        Put_values_into_the_wg(lista)
        tl_2.destroy()
    def Get_values():
        lista=[]
        if tl_2_wg_2_var.get()!='':
            lista.append(f'{tl_2_wg_2_0_var.get()} {tl_2_wg_2_var.get()}')
        if tl_2_wg_3_var.get()!='':
            lista.append(f'{tl_2_wg_3_0_var.get()} {tl_2_wg_3_var.get()}')
        if tl_2_wg_4_var.get()!='':
            lista.append(f'{tl_2_wg_4_0_var.get()} {tl_2_wg_4_var.get()}')
        return lista
    def Put_values_into_the_wg(lista):
        lista1 = []
        for item in lista:
            if item != '':
                lista1.append(item)
        string = ' + '.join(lista1)
        print(string)
        tb_0_fm_0_wg_15_var.set(string)

    #definições
    tl_width = 1000
    tl_height = 600
    tl_2 = CTkToplevel(janela_main, fg_color='WHITE')
    tl_2.geometry(f'{tl_width}x{tl_height}+200+50')
    tl_2.resizable(False,False)
    tl_2.title('SELECIONAR OS PRODUTOS VENDIDOS')
    tl_2.attributes('-topmost', 'true')

    #Var's 
    tl_2_wg_2_var=StringVar(value='')
    tl_2_wg_3_var=StringVar(value='')
    tl_2_wg_4_var=StringVar(value='')

    tl_2_wg_2_0_var = IntVar()
    tl_2_wg_3_0_var = IntVar()
    tl_2_wg_4_0_var = IntVar()
    #titlo wg
    tl_2_wg_0 = CTkLabel(tl_2, fg_color='blue', bg_color='blue',text='SELECIONE OS PRODUTOS VENDIDOS:', width= tl_width, height=30, font=fonte_b, text_color='white')
    tl_2_wg_0.place(x=0, y=0)

    #subtilo wg
    tl_2_wg_1 = CTkLabel(tl_2, text='PRODUTOS DE CABELO:', font=fonte_b, text_color='black')
    tl_2_wg_1.place(relx=0.05, rely=0.08)

    #checkboxers servicos basicos wdgs    
    tl_2_wg_2 = CTkCheckBox(tl_2, variable=tl_2_wg_2_var,checkbox_height=100, checkbox_width=100, text='Gel Comum', font=fonte_c, text_color='black', onvalue='GEL COMUM', offvalue='')
    tl_2_wg_2.place(relx=0.10, rely=0.15)
    tl_2_wg_2_0 = Spinbox(tl_2, from_=1, to=99, font='Helvetica', width=3, bg='lightblue', textvariable=tl_2_wg_2_0_var)
    tl_2_wg_2_0.place(relx=0.05, rely=0.21)
    tl_2_wg_3 = CTkCheckBox(tl_2, variable=tl_2_wg_3_var,checkbox_height=100, checkbox_width=100, text='Gel Bozzano', font=fonte_c, text_color='black', onvalue='GEL BOZZANO', offvalue='')
    tl_2_wg_3.place(relx=0.42, rely=0.15)
    tl_2_wg_3_0 = Spinbox(tl_2, from_=1, to=99, font='Helvetica', width=3, bg='lightblue', textvariable=tl_2_wg_3_0_var)
    tl_2_wg_3_0.place(relx=0.37, rely=0.21)
    tl_2_wg_4 = CTkCheckBox(tl_2, variable=tl_2_wg_4_var,checkbox_height=100, checkbox_width=100, text='Matizador', font=fonte_c, text_color='black', onvalue='MATIZADOR', offvalue='')
    tl_2_wg_4.place(relx=0.75, rely=0.15)
    tl_2_wg_4_0 = Spinbox(tl_2, from_=1, to=99, font='Helvetica', width=3, bg='lightblue', textvariable=tl_2_wg_4_0_var)
    tl_2_wg_4_0.place(relx=0.70, rely=0.21)

    #botoes wdgs
    tl_2_wg_5 = CTkButton(tl_2, state='normal',text='OK', font= fonte_b, command=lambda:ok())
    tl_2_wg_5.place(relx=0.40, rely=0.93)

def add_form_pgmt_2():
    imagem_subtrair = CTkImage(light_image=Image.open(r'images\botao_subtrair.png'), size=(30, 30 ))
    #forget
    tb_0_fm_0_wg_10_1.place_forget()#esconde o botao somar
    #wgs form pgmt 2 
    tb_0_fm_0_twg_1.place(relx=0.55, rely=0.4)
    #wgs valor
    tb_0_fm_0_twg_2.place(relx=0.63, rely=0.48)
    tb_0_fm_0_twg_3.place(relx=0.55, rely=0.48)
    #wgs botao
    tb_0_fm_0_twg_4 = CTkButton(tb_0_fm_0, width=10, height=10 , image=imagem_subtrair, text='', hover=True, fg_color='white', command=lambda:del_form_pgmt_2(), border_width=2, border_color='black', font= fonte_b)
    tb_0_fm_0_twg_4.place(relx=0.9, rely=0.39)     

    global meiospgmt
    meiospgmt=2
    print(meiospgmt)

    def del_form_pgmt_2():
        #forget
        tb_0_fm_0_twg_1.place_forget()
        tb_0_fm_0_twg_2.place_forget()
        tb_0_fm_0_twg_3.place_forget()
        sinalizer_3.place_forget()
        sinalizer_1.place_forget()

        #destroy
        tb_0_fm_0_twg_4.destroy()
        #place
        tb_0_fm_0_wg_10_1.place(relx=0.55, rely=0.39)#replace no botao subtrair
        global meiospgmt
        meiospgmt=1
        print(meiospgmt)

def tp_ProgressBarBox(title):
    try:
        global top
        top = CTkToplevel(janela_main)
        top.title(title)
        top.geometry('300x150+500+250')
        top.attributes('-topmost', 'true')
        fonte_c = CTkFont('arial', 25, 'bold')
        global pb_tp_ProgressBarBox
        pb_tp_ProgressBarBox = CTkProgressBar(top, orientation='horizontal', width=275)
        pb_tp_ProgressBarBox.set(0)
        pb_tp_ProgressBarBox.place(relx=0.05, rely=0.9)
        global lb_tp_ProgressBarBox
        lb_tp_ProgressBarBox = CTkLabel(top, text=title, font= fonte_c)
        lb_tp_ProgressBarBox.place(relx=0.25,rely=0.3)
        janela_main.update()
    except:
        print('Ocorreu um erro na funcao tp_ProgressBarBox, app.py')

#tabview

tabview = CTkTabview(janela_main, width= 1366, height=700)
tabview.place(relx=0, rely=0.065)
tab_registrar = tabview.add('  Registrar  ')
tab_movimentacoes = tabview.add('Movimentações')

### TAB REGISTRO
tb_0_fm_2_wg_1_textvar = StringVar(value=periodo)

## FRAME 0 \\ REGISTRAR ENTRADA
tb_0_fm_0_width= 650
tb_0_fm_0 = CTkFrame(tab_registrar, fg_color='white', border_width=5, border_color='blue', width= tb_0_fm_0_width, height=600)
tb_0_fm_0.place(relx=0.01, rely=0.0)

#titlo
tb_0_fm_0_wg_0 = CTkLabel(tb_0_fm_0, fg_color='blue', bg_color='blue',text='REGISTRAR ENTRADA', width= tb_0_fm_0_width, height=30, font=fonte_b)
tb_0_fm_0_wg_0.place(relx=0,rely=0)

#wgs profissional
def Toggle():
    if last_selected_profissional_var != '':
        if profissional_var.get() == last_selected_profissional_var.get():
            profissional_var.set('')
    last_selected_profissional_var.set(profissional_var.get())

tb_0_fm_0_wg_1 = CTkLabel(tb_0_fm_0, text='Profissional:', font= fonte_b, text_color='black')
tb_0_fm_0_wg_1.place(relx=0.05, rely=0.1)
profissional_var = StringVar()
last_selected_profissional_var = StringVar()
tb_0_fm_0_wg_2 = CTkRadioButton(tb_0_fm_0, text=profissionais[0], variable=profissional_var, value=profissionais[0], command=lambda:Toggle(), text_color='black', font=fonte_b, border_width_checked=10)
tb_0_fm_0_wg_2.place(relx=0.20, rely=0.1)
tb_0_fm_0_wg_2_1 = CTkRadioButton(tb_0_fm_0, text=profissionais[1], variable=profissional_var, value=profissionais[1], command=lambda:Toggle(), text_color='black', font=fonte_b, border_width_checked=10)
tb_0_fm_0_wg_2_1.place(relx=0.40, rely=0.1)
tb_0_fm_0_wg_2_2 = CTkRadioButton(tb_0_fm_0, text=profissionais[2], variable=profissional_var, value=profissionais[2], command=lambda:Toggle(), text_color='black', font=fonte_b, border_width_checked=10)
tb_0_fm_0_wg_2_2.place(relx=0.60, rely=0.1)
tb_0_fm_0_wg_2_3 = CTkRadioButton(tb_0_fm_0, text=profissionais[3], variable=profissional_var, value=profissionais[3], command=lambda:Toggle(), text_color='black', font=fonte_b, border_width_checked=10)
tb_0_fm_0_wg_2_3.place(relx=0.80, rely=0.1)
sinalizer = CTkLabel(tb_0_fm_0, text='Selecionar um profissional', text_color='red', font=fonte_sinalizer, height=4)

#wgs serviços
tb_0_fm_0_wg_4_var = StringVar(value='')
imagem_somar = CTkImage(light_image=Image.open(r'images\botao_somar.png'), size=(30, 30 ))

tb_0_fm_0_wg_3 = CTkLabel(tb_0_fm_0, text='Serviços:', font= fonte_b, text_color='black')
tb_0_fm_0_wg_3.place(relx=0.05, rely=0.25)
tb_0_fm_0_wg_4 = CTkEntry(tb_0_fm_0, textvariable=tb_0_fm_0_wg_4_var,font= fonte_b, width=400, height=30, fg_color='black')
tb_0_fm_0_wg_4.place(relx=0.20, rely=0.25)
tb_0_fm_0_wg_4.configure(state='disabled')
tb_0_fm_0_wg_5 = CTkButton(tb_0_fm_0, width=10, height=10 , image=imagem_somar, text='', hover=True, fg_color='white', command=lambda:tl_0(), border_width=2, border_color='black', font= fonte_b)
tb_0_fm_0_wg_5.place(relx=0.9, rely=0.243)

#wgs form pgmt
modo_pgmt_entrada = form_pgmt_entrada
modo_pgmt_entrada.append(' '*80)
tb_0_fm_0_wg_6 = CTkLabel(tb_0_fm_0, text='Modo Pgmt.:', font= fonte_b, text_color='black')
tb_0_fm_0_wg_6.place(relx=0.05, rely=0.4)
tb_0_fm_0_wg_7 = CTkComboBox(tb_0_fm_0,font= fonte_b, values=modo_pgmt_entrada, fg_color='black', width=200, dropdown_hover_color='blue')  
tb_0_fm_0_wg_7.place(relx=0.20, rely=0.4)
tb_0_fm_0_wg_7.set('MODO DE PGMT. 1')
sinalizer_0 = CTkLabel(tb_0_fm_0, text='Selecione uma forma de pagamento válida', text_color='red', font=fonte_sinalizer, height=4)

#wgs form pgmt 2
tb_0_fm_0_twg_1 = CTkComboBox(tb_0_fm_0,font= fonte_b, values=modo_pgmt_entrada, fg_color='black', width=200, dropdown_hover_color='blue')  
tb_0_fm_0_twg_1.place(relx=0.55, rely=0.4)
tb_0_fm_0_twg_1.set('MODO DE PGMT. 2')
tb_0_fm_0_twg_1.place_forget()
sinalizer_1 = CTkLabel(tb_0_fm_0, text='Selecione uma forma de pagamento válida', text_color='red', font=fonte_sinalizer, height=4)


tb_0_fm_0_twg_2 = CTkEntry(tb_0_fm_0, font= fonte_b, width=100, height=30, fg_color='black', placeholder_text='00,00')
tb_0_fm_0_twg_2.place(relx=0.63, rely=0.48)
tb_0_fm_0_twg_2.place_forget()
sinalizer_3 = CTkLabel(tb_0_fm_0, text='Insira um valor válido', text_color='red', font=fonte_sinalizer, height=4)
tb_0_fm_0_twg_3 = CTkLabel(tb_0_fm_0, text='R$:', font= fonte_b, text_color='black')
tb_0_fm_0_twg_3.place(relx=0.55, rely=0.48)
tb_0_fm_0_twg_3.place_forget()

#wgs valor
tb_0_fm_0_wg_9 = CTkEntry(tb_0_fm_0, font= fonte_b, width=100, height=30, fg_color='black', placeholder_text='00,00')
tb_0_fm_0_wg_9.place(relx=0.28, rely=0.48)
sinalizer_2 = CTkLabel(tb_0_fm_0, text='Insira um valor válido', text_color='red', font=fonte_sinalizer, height=4)
tb_0_fm_0_wg_10 = CTkLabel(tb_0_fm_0, text='R$:', font= fonte_b, text_color='black')
tb_0_fm_0_wg_10.place(relx=0.23, rely=0.48)
tb_0_fm_0_wg_10_1 = CTkButton(tb_0_fm_0, width=10, height=10 , image=imagem_somar, text='', hover=True, fg_color='white', command=lambda:add_form_pgmt_2(), border_width=2, border_color='black', font= fonte_b)
tb_0_fm_0_wg_10_1.place(relx=0.55, rely=0.39)

#wgs bebidas
tb_0_fm_0_wg_12_var = StringVar(value='')
tb_0_fm_0_wg_11 = CTkLabel(tb_0_fm_0, text='Bebidas:', font= fonte_b, text_color='black')
tb_0_fm_0_wg_11.place(relx=0.05, rely=0.60)
tb_0_fm_0_wg_12 = CTkEntry(tb_0_fm_0, textvariable=tb_0_fm_0_wg_12_var,font= fonte_b, width=400, height=30, fg_color='black')
tb_0_fm_0_wg_12.place(relx=0.20, rely=0.60)
tb_0_fm_0_wg_12.configure(state='disabled')
tb_0_fm_0_wg_13 = CTkButton(tb_0_fm_0, width=10, height=10 , image=imagem_somar, text='', hover=True, fg_color='white', command=lambda:tl_1(), border_width=2, border_color='black', font= fonte_b)
tb_0_fm_0_wg_13.place(relx=0.9, rely=0.593)

#wgs produtos
tb_0_fm_0_wg_15_var = StringVar(value='')
tb_0_fm_0_wg_14 = CTkLabel(tb_0_fm_0, text='Produtos:', font= fonte_b, text_color='black')
tb_0_fm_0_wg_14.place(relx=0.05, rely=0.75)
tb_0_fm_0_wg_15 = CTkEntry(tb_0_fm_0, textvariable=tb_0_fm_0_wg_15_var,font= fonte_b, width=400, height=30, fg_color='black')
tb_0_fm_0_wg_15.place(relx=0.20, rely=0.75)
tb_0_fm_0_wg_15.configure(state='disabled')
tb_0_fm_0_wg_16 = CTkButton(tb_0_fm_0, width=10, height=10 , image=imagem_somar, text='', hover=True, fg_color='white', command=lambda:tl_2(), border_width=2, border_color='black', font= fonte_b)
tb_0_fm_0_wg_16.place(relx=0.9, rely=0.743)

#botao registrar
tb_0_fm_0_wg_11 = CTkButton(tb_0_fm_0, state='normal',text='Registrar Entrada', font= fonte_b, command=lambda:RegistrarEntrada(wb))
tb_0_fm_0_wg_11.place(relx=0.40, rely=0.88)

## FRAME 1 \\ REGISTRAR SAIDA

tb_1_fm_1_width= 650
tb_1_fm_1 = CTkFrame(tab_registrar, fg_color='white', border_width=5, border_color='blue', width= 650, height=600)
tb_1_fm_1.place(relx=0.5, rely=0.0)

#titlo
tb_1_fm_1_wg_0 = CTkLabel(tb_1_fm_1, fg_color='blue', bg_color='blue', text='REGISTRAR SAÍDA', width= tb_1_fm_1_width, height=30, font=fonte_b)
tb_1_fm_1_wg_0.place(relx=0,rely=0)

#wgs despesas
desps = despesas
desps.append(' '*117)
tb_1_fm_0_wg_1 = CTkLabel(tb_1_fm_1, text='Despesa:', font= fonte_b, text_color='black')
tb_1_fm_0_wg_1.place(relx=0.05, rely=0.1)
tb_1_fm_0_wg_2 = CTkComboBox(tb_1_fm_1,font= fonte_b, values=desps, fg_color='black', width=400, dropdown_hover_color='blue')  
tb_1_fm_0_wg_2.place(relx=0.20, rely=0.1)
tb_1_fm_0_wg_2.set('SELECIONAR DESPESA')
sinalizer_4 = CTkLabel(tb_1_fm_1, text='selecione uma despesa válida', text_color='red', font=fonte_sinalizer, height=4)


#wgs form pgmt
modo_pgmt_saida = form_pgmt_saida
modo_pgmt_saida.append(' '*80)
tb_1_fm_0_wg_3 = CTkLabel(tb_1_fm_1, text='Modo Pgmt.:', font= fonte_b, text_color='black')
tb_1_fm_0_wg_3.place(relx=0.05, rely=0.25)
tb_1_fm_0_wg_4 = CTkComboBox(tb_1_fm_1,font= fonte_b, values=modo_pgmt_saida, fg_color='black', width=200, dropdown_hover_color='blue')  
tb_1_fm_0_wg_4.place(relx=0.20, rely=0.25)
tb_1_fm_0_wg_4.set('MODO DE PGMT')
sinalizer_5 = CTkLabel(tb_1_fm_1, text='Selecione uma forma de pagamento válida', text_color='red', font=fonte_sinalizer, height=4)


#wgs valor
tb_1_fm_0_wg_5 = CTkEntry(tb_1_fm_1, font= fonte_b, width=100, height=30, fg_color='black', placeholder_text='00,00')
tb_1_fm_0_wg_5.place(relx=0.65, rely=0.25)
tb_1_fm_0_wg_6 = CTkLabel(tb_1_fm_1, text='R$:', font= fonte_b, text_color='black')
tb_1_fm_0_wg_6.place(relx=0.60, rely=0.25)
sinalizer_6 = CTkLabel(tb_1_fm_1, text='Insira um valor válido', text_color='red', font=fonte_sinalizer, height=4)


#botao registrar
tb_1_fm_0_wg_7 = CTkButton(tb_1_fm_1, state='normal',text='Registrar Saída', font= fonte_b, command=lambda:RegistrarSaida())
tb_1_fm_0_wg_7.place(relx=0.40, rely=0.88)

### TAB MOVIMENTAÇÕES

#maior: FRAME 8

#  FRAME 0 \\ Upper Label

#textvars's 

frame_8_widget_0_textvar = StringVar(value=periodo)
label_0_2_textvar = StringVar(value=data)

#widget's

frame_0 = CTkFrame(janela_main, width=1350, height=50, fg_color='blue')
frame_0.place(x=0, y=0)

label_0_1 = CTkLabel(frame_0, width=100, text=f'Data:', font=fonte_c)
label_0_1.place(relx=0.41, y=10)
label_0_2 = CTkLabel(frame_0, width=99, textvariable=label_0_2_textvar, font=fonte_c, fg_color='black')
label_0_2.place(relx=0.48, y=10)

imagem_lobo = CTkImage(light_image=Image.open(r'images\imagem_lobo.png'), size=(45,45))
imagem_atualizar = CTkImage(light_image=Image.open(r'images\atualizar.png'), size=(30, 30 ))
imagem_excluir = CTkImage(light_image=Image.open(r'images\excluir.png'), size=(30, 30 ))
imagem_internet_on = CTkImage(light_image=Image.open(r'images\wifi_on.png'), size=(30, 30 ))
imagem_internet_off = CTkImage(light_image=Image.open(r'images\wifi_off.png'), size=(30, 30 ))

frame_0_widget_1 = CTkLabel(frame_0, image=imagem_lobo, text='')
frame_0_widget_1.place(x=10,y=3)
frame_0_widget_2 = CTkButton(frame_0, width=10, height=10 ,image=imagem_atualizar, text='', hover=True, fg_color='white', command=lambda:Atualizar())
frame_0_widget_2.place(x=1300, y=5)

frame_0_widgets_3 = CTkLabel(frame_0, width=80, text='Período:', font=fonte_b)
frame_0_widgets_3.place(x=50, y=10)
frame_0_widgets_4 = CTkLabel(frame_0, width=79, textvariable=frame_8_widget_0_textvar, font=fonte_b, fg_color='black')
frame_0_widgets_4.place(x=130, y=10) 

internet_connected = check_internet_connection()
if internet_connected:
    frame_0_widgets_5 = CTkLabel(frame_0, image=imagem_internet_on, text='')
    frame_0_widgets_5.place(x=1250, y=10) 
else:
    frame_0_widgets_5 = CTkLabel(frame_0, image=imagem_internet_off, text='')
    frame_0_widgets_5.place(x=1250, y=10)

#  FRAME 1  \\ Expositor faturamentos Diário

#definições pré-widget
faturamento_por_barbeiro_diario = Obter_faturamento_diario_by_barbeiro(wb, data, periodo)
tot_diario = helper.format_to_moeda(helper.format_to_float(faturamento_por_barbeiro_diario[0])+helper.format_to_float(faturamento_por_barbeiro_diario[1])+helper.format_to_float(faturamento_por_barbeiro_diario[2])+helper.format_to_float(faturamento_por_barbeiro_diario[3]))
label_1_textvar = StringVar(value=f'R${faturamento_por_barbeiro_diario[0]}')
label_3_textvar = StringVar(value=f'R${faturamento_por_barbeiro_diario[1]}')
label_5_textvar = StringVar(value=f'R${faturamento_por_barbeiro_diario[2]}')
label_7_textvar = StringVar(value=f'R${faturamento_por_barbeiro_diario[3]}')
label_9_textvar = StringVar(value=f'R${tot_diario}')

frame_1 = CTkFrame(tab_movimentacoes, width=201, height=180,border_width=1, border_color='white')
frame_1.place(relx=0.825, rely=0.02)

label_00 = CTkLabel(frame_1, width=197 ,text='Faturamento Diário', font=fonte_b, fg_color='blue')
label_00.place(x=2, y=2)

label_0 = CTkLabel(frame_1, width=98 ,text=profissionais[0], font=fonte_b, fg_color='black')
label_0.place(x=1, y=30)
label_1 = CTkLabel(frame_1, textvariable=label_1_textvar ,width=98 ,font=fonte_b, fg_color='black')
label_1.place(x=101, y=30)

label_2 = CTkLabel(frame_1, width=98 ,text=profissionais[1], font= fonte_b, fg_color='black')
label_2.place(x=1, y=60)
label_3 = CTkLabel(frame_1, textvariable=label_3_textvar ,width=98, font= fonte_b, fg_color='black') 
label_3.place(x=101, y=60)

label_4 = CTkLabel(frame_1, width=98 ,text=profissionais[2], font= fonte_b, fg_color='black')
label_4.place(x=1, y=90)
label_5 = CTkLabel(frame_1, textvariable=label_5_textvar ,width=98 , font= fonte_b, fg_color='black') 
label_5.place(x=101, y=90)

label_6 = CTkLabel(frame_1, width=98 ,text=profissionais[3], font= fonte_b, fg_color='black')
label_6.place(x=1, y=120)
label_7 = CTkLabel(frame_1, textvariable=label_7_textvar , width=98 , font= fonte_b, fg_color='black') 
label_7.place(x=101, y=120)

label_8 = CTkLabel(frame_1, width=98 ,text='TOTAL', font= fonte_b, fg_color='white', text_color='black')
label_8.place(x=1, y=150)
label_9 = CTkLabel(frame_1, textvariable=label_9_textvar , width=98 , font= fonte_b, fg_color='white', text_color='black') 
label_9.place(x=101, y=150)

#   FRAME 5 \\ Expositor faturamentos Semanal

#Expositor Faturamento semanal

#definições pré-widget
faturamento_por_barbeiro_semanal = Obter_faturamento_semanal_by_barbeiro(data, periodo)
print(faturamento_por_barbeiro_semanal)
tot_semanal = helper.format_to_float(faturamento_por_barbeiro_semanal[0])+helper.format_to_float(faturamento_por_barbeiro_semanal[1])+helper.format_to_float(faturamento_por_barbeiro_semanal[2])+helper.format_to_float(faturamento_por_barbeiro_semanal[3])
Frame_5_Widget_2_textvar = StringVar(value=f'R${faturamento_por_barbeiro_semanal[0]}')
Frame_5_Widget_4_textvar = StringVar(value=f'R${faturamento_por_barbeiro_semanal[1]}')
Frame_5_Widget_6_textvar = StringVar(value=f'R${faturamento_por_barbeiro_semanal[2]}')
Frame_5_Widget_8_textvar = StringVar(value=f'R${faturamento_por_barbeiro_semanal[3]}')
Frame_5_Widget_10_textvar = StringVar(value=f'R${tot_semanal}')

frame_5 = CTkFrame(tab_movimentacoes, width=201, height=180,border_width=1, border_color='white')
frame_5.place(relx=0.825, rely=0.32)

Frame_5_Widget_0 = CTkLabel(frame_5, width=197 ,text='Faturamento Semanal', font=fonte_b, fg_color='blue')
Frame_5_Widget_0.place(x=2, y=2)

Frame_5_Widget_1 = CTkLabel(frame_5, width=98 ,text=profissionais[0], font=fonte_b, fg_color='black')
Frame_5_Widget_1.place(x=1, y=30)
Frame_5_Widget_2 = CTkLabel(frame_5, textvariable=Frame_5_Widget_2_textvar ,width=98 ,font=fonte_b, fg_color='black')
Frame_5_Widget_2.place(x=101, y=30)

Frame_5_Widget_3 = CTkLabel(frame_5, width=98 ,text=profissionais[1], font= fonte_b, fg_color='black')
Frame_5_Widget_3    .place(x=1, y=60)
Frame_5_Widget_4 = CTkLabel(frame_5, textvariable=Frame_5_Widget_4_textvar ,width=98, font= fonte_b, fg_color='black') 
Frame_5_Widget_4.place(x=101, y=60)

Frame_5_Widget_5 = CTkLabel(frame_5, width=98 ,text=profissionais[2], font= fonte_b, fg_color='black')
Frame_5_Widget_5.place(x=1, y=90)
Frame_5_Widget_6 = CTkLabel(frame_5, textvariable=Frame_5_Widget_6_textvar ,width=98 , font= fonte_b, fg_color='black') 
Frame_5_Widget_6.place(x=101, y=90)

Frame_5_Widget_7 = CTkLabel(frame_5, width=98 ,text=profissionais[3], font= fonte_b, fg_color='black')
Frame_5_Widget_7.place(x=1, y=120)
Frame_5_Widget_8 = CTkLabel(frame_5, textvariable=Frame_5_Widget_8_textvar , width=98 , font= fonte_b, fg_color='black') 
Frame_5_Widget_8.place(x=101, y=120)

Frame_5_Widget_9 = CTkLabel(frame_5, width=98 ,text='TOTAL', font= fonte_b, fg_color='white', text_color='black')
Frame_5_Widget_9.place(x=1, y=150)
Frame_5_Widget_10 = CTkLabel(frame_5, textvariable=Frame_5_Widget_10_textvar , width=98 , font= fonte_b, fg_color='white', text_color='black') 
Frame_5_Widget_10.place(x=101, y=150)

#   FRAME 6 \\  Expositor faturamentos Mensal

#definições pré-widget
faturamento_por_barbeiro_mensal = Obter_faturamento_mensal_by_barbeiro(wb, periodo)
tot_mensal = helper.format_to_float(faturamento_por_barbeiro_mensal[0])+helper.format_to_float(faturamento_por_barbeiro_mensal[1])+helper.format_to_float(faturamento_por_barbeiro_mensal[2])+helper.format_to_float(faturamento_por_barbeiro_mensal[3])
#tot_mensal = float(faturamento_por_barbeiro_mensal[0])+float(faturamento_por_barbeiro_mensal[1])+float(faturamento_por_barbeiro_mensal[2])+float(faturamento_por_barbeiro_mensal[3])
Frame_6_Widget_2_textvar = StringVar(value=f'R${faturamento_por_barbeiro_mensal[0]}')
Frame_6_Widget_4_textvar = StringVar(value=f'R${faturamento_por_barbeiro_mensal[1]}')
Frame_6_Widget_6_textvar = StringVar(value=f'R${faturamento_por_barbeiro_mensal[2]}')
Frame_6_Widget_8_textvar = StringVar(value=f'R${faturamento_por_barbeiro_mensal[3]}')
Frame_6_Widget_10_textvar = StringVar(value=f'R${tot_mensal}')

frame_6 = CTkFrame(tab_movimentacoes, width=201, height=180,border_width=1, border_color='white')
frame_6.place(relx=0.825, rely=0.62)

Frame_6_Widget_0 = CTkLabel(frame_6, width=197 ,text='Faturamento Mensal', font=fonte_b, fg_color='blue')
Frame_6_Widget_0.place(x=2, y=2)

Frame_6_Widget_1 = CTkLabel(frame_6, width=98 ,text=profissionais[0], font=fonte_b, fg_color='black')
Frame_6_Widget_1.place(x=1, y=30)
Frame_6_Widget_2 = CTkLabel(frame_6, textvariable=Frame_6_Widget_2_textvar ,width=98 ,font=fonte_b, fg_color='black')
Frame_6_Widget_2.place(x=101, y=30)

Frame_6_Widget_3 = CTkLabel(frame_6, width=98 ,text=profissionais[1], font= fonte_b, fg_color='black')
Frame_6_Widget_3.place(x=1, y=60)
Frame_6_Widget_4 = CTkLabel(frame_6, textvariable=Frame_6_Widget_4_textvar ,width=98, font= fonte_b, fg_color='black') 
Frame_6_Widget_4.place(x=101, y=60)

Frame_6_Widget_5 = CTkLabel(frame_6, width=98 ,text=profissionais[2], font= fonte_b, fg_color='black')
Frame_6_Widget_5.place(x=1, y=90)
Frame_6_Widget_6 = CTkLabel(frame_6, textvariable=Frame_6_Widget_6_textvar ,width=98 , font= fonte_b, fg_color='black') 
Frame_6_Widget_6.place(x=101, y=90)

Frame_6_Widget_7 = CTkLabel(frame_6, width=98 ,text=profissionais[3], font= fonte_b, fg_color='black')
Frame_6_Widget_7.place(x=1, y=120)
Frame_6_Widget_8 = CTkLabel(frame_6, textvariable=Frame_6_Widget_8_textvar , width=98 , font= fonte_b, fg_color='black') 
Frame_6_Widget_8.place(x=101, y=120)

Frame_6_Widget_9 = CTkLabel(frame_6, width=98 ,text='TOTAL', font= fonte_b, fg_color='white', text_color='black')
Frame_6_Widget_9.place(x=1, y=150)
Frame_6_Widget_10 = CTkLabel(frame_6, textvariable=Frame_6_Widget_10_textvar , width=98 , font= fonte_b, fg_color='white', text_color='black') 
Frame_6_Widget_10.place(x=101, y=150)

#    FRAME 2 \\ Seção TreeView

tv = Treeview(tab_movimentacoes, columns=colunas_database , show='headings', height=20, selectmode='browse')
tv.place(relx= 0.02, rely=0.02)
tv.column('id', minwidth=30, width=30, anchor=CENTER)
tv.column('data', minwidth=50, width=50, anchor=CENTER)
tv.column('profissional', minwidth=150, width=150, anchor=CENTER)
tv.column('serviços/descrição', width=250)
tv.column('bebidas', width=150)
tv.column('produtos', width=150)
tv.column('form pgmt', width=80)
tv.column('entrada', width=70)
tv.column('saída', width=70)
tv.column('hora', width=50, anchor=CENTER)
tv.heading('id', text='ID', anchor=CENTER)
tv.heading('data', text='DATA')
tv.heading('profissional', text='PROFISSIONAL')
tv.heading('serviços/descrição', text='SERVIÇOS/DESCRIÇÃO')
tv.heading('bebidas', text='BEBIDAS')
tv.heading('produtos', text='PRODUTOS')
tv.heading('form pgmt', text='FORM. PGMT')
tv.heading('entrada', text='VALOR')
tv.heading('saída', text='SAÍDA')
tv.heading('hora', text='HORA')

vs=CTkScrollbar(tab_movimentacoes, command=tv.yview)
tv.configure(yscrollcommand=vs.set)
vs.place(relx=0.80, rely=0.02)

atendimentos_var = IntVar(value=faturamento_por_barbeiro_diario[4])
atend_wg_0 = CTkLabel(tab_movimentacoes, text='Nº ATENDIMENTOS: ', height=5)
atend_wg_0.place(relx=0.02, rely=0.68)
atend_wg_1 = CTkLabel(tab_movimentacoes, textvariable=atendimentos_var, height=5)
atend_wg_1.place(relx=0.11, rely=0.68)

LoadData()
    
# FRAME 7 \\ EXPOSITOR DO FATURAMENTOS DO DIA POR TIPO
    
#pré- widgets
faturamento_dia_by_formpgmt = Get_faturamento_dia_by_formpgmt(wb, periodo, data)
caixa = Obter_caixa(data, periodo)

#text var's

frame_7_Widget_1_textvar = StringVar(value=f'R${faturamento_dia_by_formpgmt[0]}')
frame_7_Widget_3_textvar = StringVar(value=f'R${faturamento_dia_by_formpgmt[1]}')
frame_7_Widget_5_textvar = StringVar(value=f'R${faturamento_dia_by_formpgmt[2]}')
frame_7_Widget_12_textvar = StringVar(value=f'R${faturamento_dia_by_formpgmt[3]}')   
frame_7_Widget_8_textvar = StringVar(value=f'R${caixa}')

#frame

frame_7 = CTkFrame(tab_movimentacoes, width=790, height=100, border_width=1, border_color='white')
frame_7.place(relx=0.12, rely=0.725)

#widget's

frame_7_Widget_0 = CTkLabel(frame_7, width=90 , text=' DINHEIRO ', font=fonte_b, fg_color='blue')
frame_7_Widget_0.place(x=20, y=10)
frame_7_Widget_1 = CTkLabel(frame_7, width=90 ,textvariable=frame_7_Widget_1_textvar, font=fonte_b, fg_color='black')
frame_7_Widget_1.place(x=110, y=10)

frame_7_Widget_2 = CTkLabel(frame_7, width=90 , text=' DÉBITO ', font=fonte_b, fg_color='blue')
frame_7_Widget_2.place(x=210, y=10)
frame_7_Widget_3 = CTkLabel(frame_7, width=90 ,textvariable=frame_7_Widget_3_textvar, font=fonte_b, fg_color='black')
frame_7_Widget_3.place(x=300, y=10)

frame_7_Widget_4 = CTkLabel(frame_7, width=90 , text=' CRÉDITO ', font=fonte_b, fg_color='blue')
frame_7_Widget_4.place(x=400, y=10)
frame_7_Widget_5 = CTkLabel(frame_7, width=90 ,textvariable=frame_7_Widget_5_textvar, font=fonte_b, fg_color='black')
frame_7_Widget_5.place(x=490, y=10)

frame_7_Widget_11 = CTkLabel(frame_7, width=90 , text=' PIX QR', font=fonte_b, fg_color='blue')
frame_7_Widget_11.place(x=590, y=10)
frame_7_Widget_12 = CTkLabel(frame_7, width=90 ,textvariable=frame_7_Widget_12_textvar, font=fonte_b, fg_color='black')
frame_7_Widget_12.place(x=680, y=10)

frame_7_Widget_6 = CTkButton(frame_7, text='Fechar Caixa', command=lambda:FecharCaixa(frame_7_Widget_10.get()) ,font= fonte_b)
frame_7_Widget_6.place(x=520, y=60)

frame_7_Widget_7 = CTkLabel(frame_7, width=90 , text='    CAIXA     ', font=fonte_c, fg_color='blue')
frame_7_Widget_7.place(x=20, y=60)
frame_7_Widget_8 = CTkLabel(frame_7, width=130 ,textvariable=frame_7_Widget_8_textvar, font=fonte_c, fg_color='black', text_color='green')
frame_7_Widget_8.place(x=155, y=60)

frame_7_Widget_9 = CTkLabel(frame_7, text='R$' ,font=fonte_c)
frame_7_Widget_9.place(x=325, y=60)
frame_7_Widget_10 = CTkEntry(frame_7, width=118 ,font=fonte, fg_color='black')
frame_7_Widget_10.place(x=363, y=60)

frame_7_Widget_11 = CTkButton(frame_7, width=10, height=10 ,image=imagem_excluir, text='', hover=True, fg_color='white', command=lambda:DeleteTreeviewItem())
frame_7_Widget_11.place(x=700, y=55)



janela_main.mainloop()
