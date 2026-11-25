

import os
import psycopg
from dotenv import load_dotenv

# Carrega as informações do arquivo .env
load_dotenv()

def conectar_banco():
    conexao = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    return conexao

if __name__ == "__main__":
    conexao = conectar_banco()

    print("Conexão com PostgreSQL realizada com sucesso!")

    conexao.close()
    