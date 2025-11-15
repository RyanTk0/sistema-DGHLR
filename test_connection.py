import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

try:
    conexao = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    if conexao.is_connected():
        print("Conexão com o banco de dados bem-sucedida!")
        print("Banco de dados conectado:", db_name)

except Error as e:
    print("Erro ao conectar ao banco de dados:", e)

finally:
    if 'conexao' in locals() and conexao.is_connected():
        conexao.close()
        print("Conexão encerrada.")