import sqlite3
import os
import sys
sys.path.append(".")
from Modules.variantion import openVariante



def database_exists(database):
    return os.path.exists(database)

def create_database(database):
    try:
        conn = sqlite3.connect(database)
        print(f"Banco de dados '{database}' criado com sucesso.")
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao criar o banco de dados '{database}': {e}")
        return None

def table_exists(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cursor.fetchone() is not None

def create_table(cursor, table_name, variaveis):
    create_table_sql = f"""
        CREATE TABLE {table_name} (
            {', '.join(variaveis)}
        );
    """
    cursor.execute(create_table_sql)
    print(f"Tabela '{table_name}' criada com sucesso.")

def create_tables(database, bloco):
    arquivo_variaveis = "./Database/Variation.txt"
    bloco_desejado = bloco

    # Verificar se o banco de dados já existe
    if not database_exists(database):
        conn = create_database(database)
        if conn is not None:
            try:
                cursor = conn.cursor()
                variaveis = openVariante(arquivo_variaveis, bloco_desejado)
                if variaveis:
                    create_table(cursor, bloco_desejado, variaveis)
                    conn.commit()
            finally:
                conn.close()
    else:
        try:
            conn = sqlite3.connect(database)
            cursor = conn.cursor()
            if not table_exists(cursor, bloco_desejado):
                variaveis = openVariante(arquivo_variaveis, bloco_desejado)
                if variaveis:
                    create_table(cursor, bloco_desejado, variaveis)
                    conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados '{database}': {e}")
        finally:
            if conn:
                conn.close()

# if __name__ == "__main__":
#     create_tables("usuario.db", "Usuarios")
