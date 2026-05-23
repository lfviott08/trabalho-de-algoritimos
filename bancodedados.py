import mysql.connector

def conectar():

# Conecta no banco de dados
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",  # Altere para a senha do seu banco, se for diferente
        database="eleicao"
    )
    return conexao