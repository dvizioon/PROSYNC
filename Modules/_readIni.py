import sys
sys.path.append(".")
import configparser
from tkinter import messagebox
import os

def LerINI(nome_arquivo_ini, secao, chave=None):
    if not os.path.exists(nome_arquivo_ini):
        messagebox.showerror("Erro", "Arquivo INI não encontrado")
        return None
    
    config = configparser.ConfigParser()
    config.read(nome_arquivo_ini)
    
    if secao not in config:
        messagebox.showerror("Erro", f"Seção '{secao}' não encontrada no arquivo INI")
        return None
    
    if chave is None:
        # Retorna toda a seção
        return dict(config[secao])
    else:
        if chave not in config[secao]:
            messagebox.showerror("Erro", f"Chave '{chave}' não encontrada na seção '{secao}' do arquivo INI")
            return None
        return config[secao][chave]

# Exemplo de uso:
# Retorna toda a seção
# valores = LerINI("arquivo.ini", "secao")
# if valores:
#     print(valores)

# Retorna o valor da chave específica
# valor = LerINI("arquivo.ini", "secao", "chave")
# if valor:
#     print(valor)