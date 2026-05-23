# Arquivo: criptografia.py

def caracteres_para_numeros(texto):
    """Converte texto em uma lista de números baseada em um alfabeto."""
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    numeros = []
    for letra in str(texto).upper():
        achou = False
        posicao = 0
        while posicao < len(alfabeto) and achou == False:
            if alfabeto[posicao] == letra:
                numeros.append(posicao)
                achou = True
            posicao += 1
        if achou == False:
            numeros.append(0) 
    return numeros

def numeros_para_caracteres(numeros):
    """Converte uma lista de números de volta para caracteres."""
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    texto = ""
    for num in numeros:
        texto += alfabeto[num]
    return texto

def criptografar_hill(texto):
    """
    Criptografa usando Cifra de Hill com matriz [[1, 2], [0, 1]].
    Args:
        texto (str): O texto a ser cifrado.
    Returns:
        str: Texto cifrado.
    """
    texto_formatado = str(texto).upper()
    if len(texto_formatado) % 2 != 0:
        texto_formatado += "X" 
    
    numeros = caracteres_para_numeros(texto_formatado)
    numeros_cifrados = []
    
    pos = 0
    while pos < len(numeros):
        v1 = numeros[pos]
        v2 = numeros[pos+1]
        
        # Multiplicação pela matriz e módulo 36 (tamanho do alfabeto)
        c1 = (1 * v1 + 2 * v2) % 36
        c2 = (0 * v1 + 1 * v2) % 36
        
        numeros_cifrados.append(c1)
        numeros_cifrados.append(c2)
        pos += 2
        
    return numeros_para_caracteres(numeros_cifrados)

def descriptografar_hill(texto):
    """
    Descriptografa usando a matriz inversa [[1, 34], [0, 1]].
    """
    numeros = caracteres_para_numeros(texto)
    numeros_claros = []
    
    pos = 0
    while pos < len(numeros):
        c1 = numeros[pos]
        c2 = numeros[pos+1]
        
        v1 = (1 * c1 + 34 * c2) % 36
        v2 = (0 * c1 + 1 * c2) % 36
        
        numeros_claros.append(v1)
        numeros_claros.append(v2)
        pos += 2
        
    return numeros_para_caracteres(numeros_claros).replace("X", "")