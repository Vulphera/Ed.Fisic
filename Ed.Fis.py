from datetime import datetime

def ponto_virgula(mensagem = ''):
    while True:
        entrada = str(input(mensagem).replace(',', '.')).strip()
        if entrada.isalpha():
            print(f'\033[0;31m"{entrada}" não é um valor inválido, tente novamente\033[m')
        elif entrada == '':
            print(f'\033[0;31mPor favor, digite um valor válido\033[m')
        else:
            num = float(entrada)
            return num

Cadastro_Aluno = {}
Cadastro_Aluno['Nome'] = input('Digite o Nome do Aluno: ').title()

def calcular_idade():
    
    Data_Nascimento = input('Digite Dia/Mês/Ano: ')
    Data_Nascimento = datetime.strptime(Data_Nascimento, "%d/%m/%Y") #fazer tratamento de erro para reconhecer
    Dia_de_Hoje = datetime.today()
    Idade = Dia_de_Hoje.year - Data_Nascimento.year
    if (Dia_de_Hoje.month, Dia_de_Hoje.day) < (Data_Nascimento.month, Data_Nascimento.day):
        Idade -= 1
    return Idade
    #Se possível fazer uma notificação do aniversario do infeliz

Cadastro_Aluno['Idade'] = calcular_idade()

def Sexo():
    while True:
        sexo = input('Digite o Sexo do Aluno: ').title()[0]
        if sexo == 'M':
            return 'Masculino'
        elif sexo == 'F':
            return 'Feminino'
        else:
            print('tente novamente')

Cadastro_Aluno['Sexo'] = Sexo() #Lembrar que Sexo vai ser utilizado para fazer um calculo, importante deixá-lo bem marcado

def Peso_do_Cadastrado(Peso_em_Kg = ''):
    while True:
        try:
            Peso_em_Kg = ponto_virgula('Digite o peso em Kg: ')
        except ValueError:
            print('Por favor, digite um número')
        else:
            return Peso_em_Kg

Cadastro_Aluno['Peso'] = Peso_do_Cadastrado()

def Altura_do_Cadastrado(Num = ''):
    while True:
        try:
            Altura_em_cm = ponto_virgula('Digite a altura: ')
        except ValueError:
            print('Por favor, digite um número')
        else:
            return Altura_em_cm

Cadastro_Aluno['Altura'] = Altura_do_Cadastrado('Digite a altura em metros')

def Circunferencia():
    Cincunferencia_Medidas = {}
    Cincunferencia_Medidas['Ombro'] =  ponto_virgula('Diâmetro do Ombro: ')
    Cincunferencia_Medidas['Torax'] = ponto_virgula('Diâmetro do Torax: ')
    Cincunferencia_Medidas['Cintura'] = ponto_virgula('Diâmetro da Cintura: ')
    Cincunferencia_Medidas['Abdomen'] = ponto_virgula('Diâmetro do Abdomen: ')
    Cincunferencia_Medidas['Quadril'] = ponto_virgula('Diâmetro do Quadril: ')
    Cincunferencia_Medidas['Braco_Direito'] = ponto_virgula('Diâmetro do Braço Direito: ')
    Cincunferencia_Medidas['Braco_Esquerdo'] = ponto_virgula('Diâmetro do Braço Esquerdo: ')
    Cincunferencia_Medidas['Antebraco_Direito'] = ponto_virgula('Diâmetro do Ante-braço Direito: ')
    Cincunferencia_Medidas['Antebraco_Esquerdo'] = ponto_virgula('Diâmetro do Ante-braço Esquerdo: ')
    Cincunferencia_Medidas['Coxa_Direita'] = ponto_virgula('Diâmetro da Coxa Direita: ')
    Cincunferencia_Medidas['Coxa_Esquerda'] = ponto_virgula('Diâmetro da Coxa Esquerda: ')
    Cincunferencia_Medidas['Panturrilha_Direita'] = ponto_virgula('Diâmetro da Panturrilha Direita: ')
    Cincunferencia_Medidas['Panturrilha_Esqueda'] = ponto_virgula('Diâmetro da Panturrilhaa Esquerda: ')
    return Cincunferencia_Medidas

Cadastro_Aluno['Circunferencia'] = Circunferencia()

def Sete_Dobras():
    Peitoral = ponto_virgula('Medida do Peitoral em milímetros: ')
    Triciptal = ponto_virgula('Medida do Triciptal em milímetros: ')
    Subscapular = ponto_virgula('Medida do Subscapular em milímetros: ')
    Axilar_Media = ponto_virgula('Medida da Axilar Média em milímetros: ')
    Abdominal = ponto_virgula('Medida do Abdominal em milímetros: ')
    Supra_Iliaca = ponto_virgula('Medida da Supra Ilíaca em milímetros: ')
    Coxa = ponto_virgula('Medida da Coxa em milímetros: ')
    medidas = [Peitoral, Triciptal, Subscapular, Axilar_Media, Abdominal, Supra_Iliaca, Coxa]
    return sum(medidas)

Cadastro_Aluno['Sete_Dobras'] = Sete_Dobras()   


def Percentual_de_Gordura(Idade, Sete_Dobras, Sexo):
    if Sexo == 'Masculino':
        Densidade_Corporal = 1.112 - 0.00043499 * Sete_Dobras + 0.00000055 * (Sete_Dobras**2) - 0.00028826 * Idade
        percentual = ((495/Densidade_Corporal) - 450)
        return round(percentual, 2)
    elif Sexo == 'Feminino':
        Densidade_Corporal = 1.097 - 0.00046971 * Sete_Dobras + 0.00000056 * (Sete_Dobras**2) - 0.00012828 * Idade
        percentual = ((4.95/Densidade_Corporal) - 450)
        return round(percentual, 2)

Cadastro_Aluno['Percentual_de_Gordura'] = Percentual_de_Gordura(Cadastro_Aluno['Idade'], Cadastro_Aluno['Sete_Dobras'], Cadastro_Aluno['Sexo'])

def Percentual_Residual(Percent_Gordura, Peso_total):
    Massa_Magra = Peso_total - (Peso_total*Percent_Gordura/100)
    return round(Massa_Magra, 2)


Cadastro_Aluno['Massa_Magra'] = (Percentual_Residual(Cadastro_Aluno['Percentual_de_Gordura'], Cadastro_Aluno['Peso']))


def Massa_Gorda(Peso_total, Massa_Magra ):
    Massa_Gorda = Peso_total - Massa_Magra
    return round(Massa_Gorda, 2)

Cadastro_Aluno['Massa_Gorda'] = (Massa_Gorda(Cadastro_Aluno['Peso'], Cadastro_Aluno['Massa_Magra']))



for chave, valor in Cadastro_Aluno.items():
    if isinstance(valor, dict):
        print(f'{chave}: ')
        for Nome, Medida in valor.items():
            print(f'    {Nome}: {Medida}')
    else:
        print(f'{chave}: {valor}')


