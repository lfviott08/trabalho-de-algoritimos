import datetime
import random
import criptografia
from gerenciamento import pausar_e_limpar 

def registrar_log(mensagem):
    """Registra eventos no log com data e hora exatas."""
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    arquivo = open("logs_urna.txt", "a", encoding="utf-8")
    arquivo.write(f"[{agora}] {mensagem}\n")
    arquivo.close()

def validar_credenciais(cursor, titulo, cpf_4, chave, perfil):
    """Valida puxando o Título e descriptografando o CPF e a Chave do banco."""
    cursor.execute(f"SELECT CPF_Eleitor, mesario, chave_acesso FROM Eleitores WHERE titulo_eleitoral = '{titulo}'")
    res = cursor.fetchall()
    
    if len(res) > 0:
        cpf_real = criptografia.descriptografar_hill(res[0][0])
        chave_real = criptografia.descriptografar_hill(res[0][2])
        
        # Verifica se os 4 primeiros dígitos e a chave batem
        if cpf_real[0:4] == cpf_4 and chave_real == chave.upper():
            if (perfil == "mesario" and res[0][1] == 1) or perfil == "eleitor":
                return True
    return False

def abrir_votacao(conexao, cursor):
    """Autentica o mesário, executa a Zerézima e abre a urna."""
    print("\n--- ABERTURA DO SISTEMA DE VOTAÇÃO ---")
    titulo = input("Digite o título de eleitor do mesário: ")
    cpf_4 = input("Digite os 4 primeiros dígitos do CPF: ")
    chave = input("Digite a chave de acesso: ")

    if validar_credenciais(cursor, titulo, cpf_4, chave, "mesario") == False:
        print("\n[Erro] Falha na validação do mesário. Acesso negado.")
        registrar_log("ALERTA: Tentativa de acesso negado")
        pausar_e_limpar()
        return False

    # Zerézima
    cursor.execute("DELETE FROM Votos")
    cursor.execute("UPDATE Eleitores SET ja_votou = FALSE")
    conexao.commit()
    
    print("\n--- ZERÉZIMA CONCLUÍDA ---")
    cursor.execute("SELECT digito_candidatos, nome_candidato FROM Candidatos")
    candidatos = cursor.fetchall()
    
    if len(candidatos) > 0:
        for cand in candidatos:
            print(f"Candidato: {cand[1]} | Número: {cand[0]} | Votos: 0")
    else:
        print("Nenhum candidato registado na base de dados.")

    registrar_log("ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")
    print("\n[Sistema] Votação aberta com sucesso!")
    pausar_e_limpar()
    return True

def realizar_voto(conexao, cursor):
    """Identifica o eleitor e registra o voto com protocolo criptografado."""
    print("\n--- IDENTIFICAÇÃO DO ELEITOR ---")
    titulo = input("Digite seu título de eleitor: ")
    cpf_4 = input("Digite os 4 primeiros dígitos do seu CPF: ")
    chave = input("Digite sua chave de acesso: ")

    if validar_credenciais(cursor, titulo, cpf_4, chave, "eleitor") == False:
        print("\n[Erro] Dados inválidos ou incorretos.")
        registrar_log("ALERTA: Tentativa de acesso negado")
        pausar_e_limpar()
        return

    cursor.execute(f"SELECT id_eleitor, ja_votou FROM Eleitores WHERE titulo_eleitoral = '{titulo}'")
    info_eleitor = cursor.fetchall()[0]
    
    if info_eleitor[1] == 1:
        print("\n[Erro] Eleitor já votou.")
        registrar_log("ALERTA: Tentativa de voto duplo")
        pausar_e_limpar()
        return

    # Laço de repetição caso o eleitor não confirme o voto
    confirmado = "NAO"
    while confirmado == "NAO":
        num = input("\nNúmero do candidato: ")
        cursor.execute(f"SELECT nome_candidato, partido_candidatos, id_candidatos FROM Candidatos WHERE digito_candidatos = '{num}'")
        res_cand = cursor.fetchall()

        if len(res_cand) > 0:
            print(f"Você está votando em: {res_cand[0][0]} ({res_cand[0][1]})")
            id_cand = res_cand[0][2]
        else:
            print("Candidato não encontrado. Votando NULO/BRANCO.")
            cursor.execute("SELECT id_candidatos FROM Candidatos WHERE digito_candidatos = 99")
            id_cand = cursor.fetchall()[0][0]

        if input("Confirma o voto? (Sim/Não): ").upper() == "SIM":
            confirmado = "SIM" # Sai do laço
            
            # Gerador de protocolo: V + 2 letras + 26 + Num (2 dígitos) + 5 números
            letras = chr(random.randint(65, 90)) + chr(random.randint(65, 90))
            num_form = num if len(num) >= 2 else "0" + num
            numeros = str(random.randint(10000, 99999))
            protocolo = f"V{letras}26{num_form}{numeros}"
            
            prot_cripto = criptografia.criptografar_hill(protocolo)
            data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("INSERT INTO Votos (digito_candidato, data_hora, protocolo, id_candidatos) VALUES (%s, %s, %s, %s)", (num, data, prot_cripto, id_cand))
            cursor.execute(f"UPDATE Eleitores SET ja_votou = TRUE WHERE id_eleitor = {info_eleitor[0]}")
            conexao.commit()

            registrar_log("SUCESSO: Voto realizado com sucesso")
            print(f"\n[Sucesso] Guarde seu protocolo: {protocolo}")
        else:
            print("\nVoto não confirmado. Retornando para a escolha do candidato...")

    pausar_e_limpar()

def encerrar_votacao(conexao, cursor):
    """Encerra a urna exigindo dupla confirmação do mesário."""
    print("\n--- ENCERRAMENTO ---")
    titulo = input("Título do mesário: ")
    cpf_4 = input("4 primeiros dígitos do CPF: ")
    chave = input("Chave de acesso: ")

    if validar_credenciais(cursor, titulo, cpf_4, chave, "mesario") == False:
        print("\n[Erro] Acesso negado.")
        registrar_log("ALERTA: Tentativa de encerramento não autorizada")
        pausar_e_limpar()
        return False

    if input("\nDeseja realmente encerrar a votação? (Sim/Não): ").upper() == "NAO":
        print("Encerramento cancelado.")
        pausar_e_limpar()
        return False
        
    chave_conf = input("Digite sua chave de acesso novamente para confirmar: ")
    if chave_conf.upper() != chave.upper():
        print("\n[Erro] Chave de confirmação incorreta. Encerramento cancelado.")
        pausar_e_limpar()
        return False

    registrar_log("ENCERRAMENTO: Votação encerrada com sucesso.")
    print("\n[Sistema] Votação encerrada com sucesso! O sistema será desligado.")
    pausar_e_limpar()
    return True
