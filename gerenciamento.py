# Arquivo: gerenciamento.py
import os
import time
import criptografia
from validacao import validar_cpf, validar_titulo, gerar_chave_acesso

def pausar_e_limpar():
    """Gera uma pausa de 2 segundos e limpa o terminal usando o comando do sistema."""
    print("\nAguarde...")
    time.sleep(4)  
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_para_leitura():
    """Pausa a tela até o usuário apertar ENTER e limpa o terminal."""
    input("\n[ Pressione ENTER para voltar ao menu... ]")
    os.system('cls' if os.name == 'nt' else 'clear')

def cadastrar_eleitor(cursor, conexao):
    """Realiza o cadastro em loop de novos eleitores no banco."""
    continuar_cadastro = "S"
    
    while continuar_cadastro == "S":
        print("\n--- CADASTRO DE NOVO ELEITOR ---")
        nome = input("Nome completo: ")
        titulo = input("Título de eleitor (12 dígitos numéricos): ")
        
        if not validar_titulo(titulo):
            print("\n[Erro] Título de eleitor inválido segundo o cálculo verificador.")
        else:
            cpf = input("CPF (11 dígitos numéricos): ")
            if not validar_cpf(cpf):
                print("\n[Erro] CPF inválido segundo o cálculo verificador.")
            else:
                cpf_cifrado_busca = criptografia.criptografar_hill(cpf)
                cursor.execute(f"SELECT * FROM Eleitores WHERE CPF_Eleitor = '{cpf_cifrado_busca}' OR titulo_eleitoral = '{titulo}'")
                
                if len(cursor.fetchall()) > 0:
                    print("\n[Erro] CPF ou Título já constam na nossa base de dados.")
                else:
                    resp_mesario = input("O eleitor será mesário? (S/N): ").upper()
                    mesario = True if resp_mesario == 'S' else False
                    
                    chave = gerar_chave_acesso(nome)
                    cpf_cripto = criptografia.criptografar_hill(cpf)
                    chave_cripto = criptografia.criptografar_hill(chave)

                    sql = "INSERT INTO Eleitores (titulo_eleitoral, nome_eleitor, CPF_Eleitor, mesario, chave_acesso, ja_votou) VALUES (%s, %s, %s, %s, %s, %s)"
                    valores = (titulo, nome, cpf_cripto, mesario, chave_cripto, False)

                    cursor.execute(sql, valores)
                    conexao.commit()
                    print(f"\n[Sucesso] Eleitor cadastrado! Anote a Chave de Acesso (Original): {chave}")
        
        continuar_cadastro = input("\nDeseja cadastrar outro eleitor? (S/N): ").upper()
        os.system('cls' if os.name == 'nt' else 'clear')

    pausar_e_limpar()

def buscar_eleitor(cursor):
    """Realiza a busca de um eleitor específico informando o CPF ou Título."""
    print("\n--- BUSCA DE ELEITOR ---")
    print("1 - Buscar por CPF")
    print("2 - Buscar por Título")
    opcao = input("Escolha a opção de busca: ")
    
    if opcao == "1":
        cpf = input("Digite o CPF (apenas números): ")
        cpf_cripto = criptografia.criptografar_hill(cpf)
        cursor.execute(f"SELECT nome_eleitor, CPF_Eleitor, titulo_eleitoral, mesario FROM Eleitores WHERE CPF_Eleitor = '{cpf_cripto}'")
    elif opcao == "2":
        titulo = input("Digite o Título (apenas números): ")
        cursor.execute(f"SELECT nome_eleitor, CPF_Eleitor, titulo_eleitoral, mesario FROM Eleitores WHERE titulo_eleitoral = '{titulo}'")
    else:
        print("\n[Erro] Opção inválida.")
        pausar_e_limpar()
        return

    resultado = cursor.fetchall()
    if len(resultado) == 0:
        print("\n[Aviso] Nenhum eleitor encontrado com os dados informados.")
    else:
        print("\nRESULTADO DA BUSCA:")
        for eleitor in resultado:
            perfil = "Mesário" if eleitor[3] == 1 else "Eleitor Comum"
            cpf_limpo = criptografia.descriptografar_hill(eleitor[1])
            print(f"Nome: {eleitor[0]} | CPF: {cpf_limpo} | Título: {eleitor[2]} | Perfil: {perfil}")
            
    pausar_para_leitura()

def listar_eleitores(cursor):
    """Lista todos os eleitores cadastrados no banco de dados."""
    print("\n--- LISTA DE ELEITORES CADASTRADOS ---")
    cursor.execute("SELECT id_eleitor, nome_eleitor, CPF_Eleitor, titulo_eleitoral, mesario FROM Eleitores")
    eleitores = cursor.fetchall()
    
    if len(eleitores) == 0:
        print("\n[Aviso] Nenhum eleitor cadastrado na base de dados.")
    else:
        for eleitor in eleitores:
            perfil = "Mesário" if eleitor[4] == 1 else "Eleitor Comum"
            cpf_limpo = criptografia.descriptografar_hill(eleitor[2])
            print(f"ID: {eleitor[0]} | Nome: {eleitor[1]} | CPF: {cpf_limpo} | Título: {eleitor[3]} | Perfil: {perfil}")
            
    pausar_para_leitura()

def editar_eleitor(cursor, conexao):
    """Permite editar nome, título, CPF e perfil do eleitor."""
    print("\n--- EDITAR DADOS DO ELEITOR ---")
    titulo_atual = input("Digite o Título do eleitor que deseja editar: ")

    cursor.execute(f"SELECT nome_eleitor, CPF_Eleitor, mesario, titulo_eleitoral FROM Eleitores WHERE titulo_eleitoral = '{titulo_atual}'")
    resultado = cursor.fetchall()

    if len(resultado) == 0:
        print("\n[Erro] Eleitor não encontrado.")
    else:
        eleitor = resultado[0]
        cpf_limpo = criptografia.descriptografar_hill(eleitor[1])
        perfil_atual = "Sim" if eleitor[2] == 1 else "Não"

        print(f"\nDados atuais -> Nome: {eleitor[0]} | Título: {eleitor[3]} | CPF: {cpf_limpo} | Mesário: {perfil_atual}")
        print("\n[ DICA: Aperte ENTER deixando em branco caso não queira alterar um dado ]\n")
        
        novo_nome = input("Novo nome: ")
        if novo_nome == "":
            novo_nome = eleitor[0]

        novo_titulo = input("Novo Título (12 dígitos numéricos): ")
        if novo_titulo == "":
            novo_titulo = eleitor[3]
        else:
            if not validar_titulo(novo_titulo):
                print("\n[Erro] O novo Título informado é inválido matematicamente.")
                pausar_e_limpar()
                return
            cursor.execute(f"SELECT * FROM Eleitores WHERE titulo_eleitoral = '{novo_titulo}'")
            if len(cursor.fetchall()) > 0:
                print("\n[Erro] Este Título já está cadastrado no sistema.")
                pausar_e_limpar()
                return

        novo_cpf = input("Novo CPF (11 dígitos numéricos): ")
        if novo_cpf == "":
            cpf_cripto_final = eleitor[1] 
        else:
            if not validar_cpf(novo_cpf):
                print("\n[Erro] O novo CPF informado é inválido matematicamente.")
                pausar_e_limpar()
                return
            cpf_cripto_busca = criptografia.criptografar_hill(novo_cpf)
            cursor.execute(f"SELECT * FROM Eleitores WHERE CPF_Eleitor = '{cpf_cripto_busca}'")
            if len(cursor.fetchall()) > 0:
                print("\n[Erro] Este CPF já está cadastrado no sistema.")
                pausar_e_limpar()
                return
            cpf_cripto_final = cpf_cripto_busca

        novo_perfil = input("Será mesário? (S/N): ").upper()
        if novo_perfil == "":
            novo_mesario = eleitor[2]
        elif novo_perfil == "S":
            novo_mesario = True
        else:
            novo_mesario = False

        cursor.execute("UPDATE Eleitores SET nome_eleitor = %s, titulo_eleitoral = %s, CPF_Eleitor = %s, mesario = %s WHERE titulo_eleitoral = %s", 
                       (novo_nome, novo_titulo, cpf_cripto_final, novo_mesario, titulo_atual))
        conexao.commit()
        print("\n[Sucesso] Dados do eleitor updated com segurança!")

    pausar_e_limpar()

def remover_eleitor(cursor, conexao):
    """Remove definitivamente um eleitor do banco de dados informando CPF ou Título."""
    print("\n--- REMOVER ELEITOR ---")
    print("1 - Remover por CPF")
    print("2 - Remover por Título")
    opcao = input("Escolha a opção: ")

    if opcao == "1":
        cpf = input("Digite o CPF do eleitor que deseja remover (apenas números): ")
        cpf_cripto = criptografia.criptografar_hill(cpf)
        cursor.execute(f"SELECT nome_eleitor, titulo_eleitoral FROM Eleitores WHERE CPF_Eleitor = '{cpf_cripto}'")
    elif opcao == "2":
        titulo = input("Digite o Título do eleitor que deseja remover (apenas números): ")
        cursor.execute(f"SELECT nome_eleitor, titulo_eleitoral FROM Eleitores WHERE titulo_eleitoral = '{titulo}'")
    else:
        print("\n[Erro] Opção inválida.")
        pausar_e_limpar()
        return

    resultado = cursor.fetchall()

    if len(resultado) == 0:
        print("\n[Erro] Eleitor não encontrado.")
    else:
        nome = resultado[0][0]
        titulo_banco = resultado[0][1] 
        
        confirma = input(f"Tem certeza que deseja remover o eleitor {nome}? (S/N): ").upper()
        
        if confirma == 'S':
            cursor.execute(f"DELETE FROM Eleitores WHERE titulo_eleitoral = '{titulo_banco}'")
            conexao.commit()
            print("\n[Sucesso] Eleitor removido com sucesso.")
        else:
            print("\nRemoção cancelada.")

    pausar_e_limpar()