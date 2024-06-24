# main.py
import sys
sys.path.append(".")
from App import criar_aplicacao
from Modules._readIni import LerINI

ini = LerINI(".INI","Host")
# print(ini)

# Criando uma instância da aplicação Flask
app = criar_aplicacao()

# Iniciando o servidor
if __name__ == "__main__":
    app.run(host=ini['host'] , port=ini['port'] ,debug=ini['debug'])
