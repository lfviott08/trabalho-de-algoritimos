
from gerenciamento import pausar_para_leitura

def exibir_logs():

    print("\n--- EXIBIÇÃO DE LOGS DE OCORRÊNCIAS ---")
    
    try:
        # O 'with' garante que o arquivo seja fechado automaticamente após a leitura
        with open("logs_urna.txt", "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
            print(conteudo)
    except FileNotFoundError:
        # Tratamento de erro exato como ensinado nos slides do professor
        print("\n[Aviso] Nenhum log encontrado. A urna ainda não registou eventos.")
        
    # Usa a pausa de leitura para a tela não sumir
    pausar_para_leitura()


def exibir_protocolos(cursor):

    print("\n--- EXIBIÇÃO DOS PROTOCOLOS DE VOTAÇÃO ---")
    
    # O comando ORDER BY protocolo ASC garante a ordem alfabética exigida no PDF
    cursor.execute("SELECT protocolo FROM Votos ORDER BY protocolo ASC")
    protocolos = cursor.fetchall()
    
    if len(protocolos) == 0:
        print("\n[Aviso] Nenhum protocolo registado até ao momento.")
    else:
        for p in protocolos:
            print(f"Protocolo Validado: {p[0]}")
            
    # Usa a pausa de leitura para a tela não sumir
    pausar_para_leitura()
