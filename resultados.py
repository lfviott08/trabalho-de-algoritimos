# Arquivo: resultados.py
from gerenciamento import pausar_para_leitura

def boletim_urna(cursor):
    """Exibe o boletim final com candidatos ordenados e declara o vencedor."""
    print("\n--- BOLETIM DE URNA ---")
    cursor.execute("""
        SELECT c.nome_candidato, c.digito_candidatos, c.partido_candidatos, COUNT(v.id_voto) as total_votos
        FROM Candidatos c
        LEFT JOIN Votos v ON c.id_candidatos = v.id_candidatos
        GROUP BY c.id_candidatos, c.nome_candidato, c.digito_candidatos, c.partido_candidatos
        ORDER BY c.nome_candidato ASC
    """)
    resultados = cursor.fetchall()
    
    maior_voto = -1
    vencedor = None
    
    for linha in resultados:
        print(f"Candidato: {linha[0]} | Número: {linha[1]} | Partido: {linha[2]} | Votos: {linha[3]}")
        if linha[3] > maior_voto:
            maior_voto = linha[3]
            vencedor = linha
            
    if vencedor != None and maior_voto > 0:
        print("\n--- VENCEDOR DA ELEIÇÃO ---")
        print(f"Nome: {vencedor[0]} | Número: {vencedor[1]} | Partido: {vencedor[2]} | Total de Votos: {maior_voto}")
    else:
        print("\nNenhum voto foi registrado ou houve empate absoluto (0 votos).")
        
    pausar_para_leitura()

def estatistica_comparecimento(cursor):
    """Exibe quantidade de pessoas que votaram e percentual."""
    print("\n--- ESTATÍSTICA DE COMPARECIMENTO ---")
    cursor.execute("SELECT COUNT(*) FROM Eleitores")
    total_eleitores = cursor.fetchall()[0][0]
    
    cursor.execute("SELECT COUNT(*) FROM Eleitores WHERE ja_votou = TRUE")
    total_votaram = cursor.fetchall()[0][0]
    
    if total_eleitores > 0:
        percentual = (total_votaram / total_eleitores) * 100
    else:
        percentual = 0
        
    print(f"Total de eleitores aptos: {total_eleitores}")
    print(f"Total de eleitores que votaram: {total_votaram}")
    print(f"Percentual de comparecimento: {percentual:.2f}%")
    pausar_para_leitura()

def votos_por_partido(cursor):
    """Soma e exibe os votos agrupados por legenda partidária."""
    print("\n--- VOTOS POR PARTIDO ---")
    cursor.execute("""
        SELECT c.partido_candidatos, COUNT(v.id_voto)
        FROM Candidatos c
        JOIN Votos v ON c.id_candidatos = v.id_candidatos
        GROUP BY c.partido_candidatos
        ORDER BY COUNT(v.id_voto) DESC
    """)
    resultados = cursor.fetchall()
    
    if len(resultados) == 0:
        print("Nenhum voto computado para partidos.")
    else:
        for linha in resultados:
            print(f"Partido: {linha[0]} | Total de Votos: {linha[1]}")
    pausar_para_leitura()

def validacao_integridade(cursor):
    """Compara o número de votos registrados fisicamente na tabela com os eleitores com status TRUE."""
    print("\n--- VALIDAÇÃO DE INTEGRIDADE ---")
    cursor.execute("SELECT COUNT(*) FROM Votos")
    total_votos_urna = cursor.fetchall()[0][0]
    
    cursor.execute("SELECT COUNT(*) FROM Eleitores WHERE ja_votou = TRUE")
    total_eleitores_votaram = cursor.fetchall()[0][0]
    
    print(f"Total de votos armazenados: {total_votos_urna}")
    print(f"Total de eleitores marcados como 'Já Votou': {total_eleitores_votaram}")
    
    if total_votos_urna == total_eleitores_votaram:
        print("\n[Status] INTEGRIDADE CONFIRMADA. O processo ocorreu sem divergências.")
    else:
        print("\n[Status] ALERTA DE DIVERGÊNCIA! A auditoria falhou.")
    pausar_para_leitura()