# Arquivo: validacao.py
import random

def validar_cpf(cpf):
    """Verifica se o CPF informado é válido."""
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
        
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto
        
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto
        
    if str(digito1) == cpf[9] and str(digito2) == cpf[10]:
        return True
    return False

def validar_titulo(titulo):
    """Verifica se o Título de Eleitor informado é válido"""
    if len(titulo) != 12:
        return False
        
    soma1 = 0
    multiplicadores1 = [2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(8):
        soma1 += int(titulo[i]) * multiplicadores1[i]
    
    resto1 = soma1 % 11
    uf = titulo[8:10]
    
    if resto1 == 10:
        dv1 = 0
    elif resto1 == 0 and (uf == '01' or uf == '02'):
        dv1 = 1
    else:
        dv1 = resto1
        
    soma2 = int(titulo[8]) * 7 + int(titulo[9]) * 8 + dv1 * 9
    resto2 = soma2 % 11
    
    if resto2 == 10:
        dv2 = 0
    elif resto2 == 0 and (uf == '01' or uf == '02'):
        dv2 = 1
    else:
        dv2 = resto2
        
    if str(dv1) == titulo[10] and str(dv2) == titulo[11]:
        return True
    return False

def gerar_chave_acesso(nome):
    """Gera uma chave de acesso automática para o eleitor."""
    partes = nome.split()
    if len(partes) > 1:
        letras = (partes[0][:2] + partes[1][0]).upper()
    else:
        letras = partes[0][:3].upper()
        
    numeros = ""
    for i in range(4):
        numeros += str(random.randint(0, 9))
        
    return letras + numeros