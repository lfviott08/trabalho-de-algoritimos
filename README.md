# ES-PI1-2026-T2-G07

O LAD.Py é o backend de um sistema de votação digital fictício executado via terminal de comandos. Este projeto foi concebido com finalidade estritamente didática para a disciplina de Projeto Integrador I (Engenharia de Software - PUC Campinas). O sistema permite o cadastramento e gestão de eleitores e candidatos, abertura de urna com processo de zerézima, validação de votação para impedir voto duplo, auditoria através de logs de ocorrências e geração de boletim de urna.

Nome dos integrantes

Eduardo Teixeira
Felipe Ferraz
João Vitor Iha
Gabriel Gambaroni
Luiz Felipe Viotto Martins

Tecnologias utilizadas:

Linguagem de Programação: Python
Banco de Dados: MySQL
Bibliotecas Python: mysql.connector, os, time, random, datetime
Instruções claras para execução do sistema

1. Preparação do Banco de Dados

Certifique-se de ter o MySQL Server instalado na sua máquina.
Abra o seu gerenciador de banco de dados (ex: MySQL Workbench).
Execute todo o código contido no ficheiro Database_eleicoes_PI.sql para criar o banco de dados eleicao, construir as tabelas com as chaves estrangeiras corretas e inserir os dados fictícios para teste.
2. Configuração do Python

É necessário ter o Python instalado.
Instale o conector do MySQL executando o seguinte comando no seu terminal: pip install mysql-connector-python
3. Configuração de Acesso

Abra o ficheiro bancodedados.py na pasta do projeto.
Altere o campo password="123456" para a senha real do utilizador root do seu MySQL local.
4. Execução

Abra o terminal ou prompt de comando na pasta raiz do projeto.
Execute o ficheiro principal com o comando: python main.py