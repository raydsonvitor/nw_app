def Search_word_in_database(codigo_dialetico):
    if codigo_dialetico in palavras:
        return True
    else:
        return False
def Recognize_tonalidade(codigo_dialetico):
    if codigo_dialetico[-1] == '!':
        return 'exclamativo'
    elif codigo_dialetico[-1] == '?':
        return 'interrogativo'
    else:
        return 'afirmativo'

palavras = ['oi', 'olá']
pontos = ['?', '!', '.']

while True:
    codigo_dialetico= input('Digite algo:').split(' ')
    step_feedback = Search_word_in_database(codigo_dialetico[0])
    codigo_dialetico_tonalidade = Recognize_tonalidade(codigo_dialetico[1])
    if step_feedback == True:
        print(f'Reconheci esta palavra: {codigo_dialetico[0]}, tonalidade contida: {codigo_dialetico_tonalidade}')
    else:
        print(f'Não reconheci esta palavra: {codigo_dialetico[0]}') 
    