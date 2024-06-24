import sys
sys.path.append(".")
import sqlite3
import os
from Modules._readIni import LerINI

ini = LerINI(".INI","paths")
# print(ini)


class ControllerUsuario:
    def __init__(self, nome_banco):
        self.nome_banco = nome_banco
        self.caminho_banco = os.path.join(ini['database'], self.nome_banco)
        self.conn = None
        self.cursor = None
        self.conectar()

    def conectar(self):
        try:
            self.conn = sqlite3.connect(self.caminho_banco)
            self.cursor = self.conn.cursor()
            # print(f"Conexão com o banco de dados '{self.caminho_banco}' estabelecida com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def fechar_conexao(self):
        if self.conn:
            self.conn.close()
            print("Conexão com o banco de dados fechada.")

    def cadastrar_usuario(self, nome, email, senha):
        try:
            self.cursor.execute("""
                INSERT INTO Usuarios (nome, email, senha) VALUES (?, ?, ?)
            """, (nome, email, senha))
            self.conn.commit()
            print(f"Usuário '{nome}' cadastrado com sucesso.")
        except sqlite3.IntegrityError as e:
            print(f"Erro ao cadastrar usuário. Email '{email}' já existe.")
        except sqlite3.Error as e:
            print(f"Erro ao cadastrar usuário: {e}")

    def listar_usuarios(self):
        try:
            if self.cursor:
                self.cursor.execute("SELECT * FROM Usuarios")
                usuarios = self.cursor.fetchall()
                return usuarios if usuarios else []
            else:
                print("Cursor não inicializado corretamente.")
                return []
        except sqlite3.Error as e:
            print(f"Erro ao listar usuários: {e}")
            return []


    def buscar_usuario_por_id(self, usuario_id):
        try:
            self.cursor.execute("SELECT * FROM Usuarios WHERE id = ?", (usuario_id,))
            usuario = self.cursor.fetchone()
            return usuario
        except sqlite3.Error as e:
            print(f"Erro ao buscar usuário por ID: {e}")
            return None

    def atualizar_usuario(self, usuario_id, nome, email, senha):
        try:
            self.cursor.execute("""
                UPDATE Usuarios SET nome = ?, email = ?, senha = ? WHERE id = ?
            """, (nome, email, senha, usuario_id))
            self.conn.commit()
            print(f"Usuário ID {usuario_id} atualizado com sucesso.")
        except sqlite3.IntegrityError as e:
            print(f"Erro ao atualizar usuário. Email '{email}' já existe.")
        except sqlite3.Error as e:
            print(f"Erro ao atualizar usuário: {e}")

    def deletar_usuario(self, usuario_id):
        try:
            self.cursor.execute("DELETE FROM Usuarios WHERE id = ?", (usuario_id,))
            self.conn.commit()
            print(f"Usuário ID {usuario_id} deletado com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao deletar usuário: {e}")

    def autenticar_usuario(self, email, senha):
        try:
            self.cursor.execute("SELECT * FROM Usuarios WHERE email = ? AND senha = ?", (email, senha))
            usuario = self.cursor.fetchone()
            if usuario:
                print(f"Usuário autenticado com sucesso: {usuario}")
                return usuario
            else:
                print("Credenciais inválidas. Falha na autenticação.")
                return None
        except sqlite3.Error as e:
            print(f"Erro ao autenticar usuário: {e}")
            return None

