import sys
import os
from flask import Flask
sys.path.append(".")
from Router.router import main_blueprint
from Api._apiUsuarios import api_usuarios
from Database.database import init_db
from Modules._readIni import LerINI
from flask_jwt_extended import JWTManager
from middleware.midleware import connect_db

# Carregar chaves do arquivo .INI
secret_key = LerINI(".INI", "secret")
_dbPath = LerINI(".INI", "paths")

def criar_aplicacao():
    app = Flask(__name__)

    # Configurar a chave secreta para o Flask
    app.config['SECRET_KEY'] = secret_key['secret_key']

    # Configurar a chave secreta para JWT
    app.config['JWT_SECRET_KEY'] = secret_key['secret_key']

    # Inicializar JWTManager
    jwt = JWTManager(app)

    # Configurar diretório estático
    app.static_folder = 'Assets'
    app.static_url_path = '/static'

    # Construir o caminho do banco de dados
    database_path = os.path.join(_dbPath['database'], _dbPath['name_db'])

    # Conectar middleware para o banco de dados
    connect_db(database_path)(app)

    # Registrar blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_usuarios)

    # Inicializar o banco de dados
    with app.app_context():
        init_db()

    return app

# if __name__ == "__main__":
#     app = criar_aplicacao()
#     app.run(debug=True)
