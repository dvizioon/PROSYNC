# app/router_api.py

import sys
sys.path.append(".")
from datetime import timedelta
from flask import Blueprint, jsonify, request, g,session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from Controller.usuarioController import ControllerUsuario
from Modules._readIni import LerINI
from middleware.midleware import connect_db, autenticador


# Carregar configurações iniciais
ini_basic = LerINI(".INI", "Usuario")
ini_rotas = LerINI(".INI", "rotas_usuarios")

# Configurar o blueprint para a API de usuários
api_usuarios = Blueprint(ini_basic['_prex'], __name__, url_prefix='/api')
database_path = ini_basic['database']

# Validação de token de autenticação
def validar_token(token):
    if token:
        parts = token.split()
        return len(parts) == 2 and parts[0].lower() == 'bearer' and parts[1] == ini_rotas['token']
    return False

# Middleware para conectar ao banco de dados antes de cada requisição
@api_usuarios.before_app_request
def before_request():
    g.db = ControllerUsuario(database_path)
    g.db.conectar()

# Middleware para fechar a conexão com o banco de dados após cada requisição
@api_usuarios.teardown_app_request
def teardown_request(exception=None):
    db = getattr(g, 'db', None)
    if db is not None:
        db.fechar_conexao()

# Rota para autenticar o usuário e gerar o token JWT
@api_usuarios.route('/authenticate', methods=['POST'])
def authenticate_user(_email,_password):
    # data = request.json
    # email = data.get('email')
    # senha = data.get('senha')
    email = _email
    senha = _password
    
    if not email or not senha:
        return jsonify({'message': 'Email e senha são obrigatórios.'}), 400
    
    usuario = g.db.autenticar_usuario(email, senha)
    if usuario:
        access_token = create_access_token(identity=email, expires_delta=timedelta(hours=1))

        session['logado'] = {
            'status':True,
            'message': 'Autenticação bem-sucedida.', 
            'access_token': access_token, 
            'usuario': usuario,
            'email':email,
            }
        
        # return jsonify({'message': 'Autenticação bem-sucedida.', 'access_token': access_token, 'usuario': usuario}), 200
        return True
    else:
        return False
        # return jsonify({'message': 'Credenciais inválidas. Falha na autenticação.'}), 401

# Rota para listar os usuários (autenticador é aplicado como middleware)
@api_usuarios.route(ini_rotas['show'], methods=['GET'])
@autenticador
def show_users():
    current_user = get_jwt_identity()  
    users = g.db.listar_usuarios()
    return jsonify(users), 200

# Rota para criar um novo usuário
@api_usuarios.route(ini_rotas['create'], methods=['POST'])
@autenticador
def create_user():
    current_user = get_jwt_identity()  
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    
    if not nome or not email or not senha:
        return jsonify({'message': 'Dados incompletos. Todos os campos são obrigatórios.'}), 400
    
    try:
        g.db.cadastrar_usuario(nome, email, senha)
        return jsonify({'message': f'Usuário {nome} cadastrado com sucesso.'}), 201
    except Exception as e:
        return jsonify({'message': f'Erro ao cadastrar usuário: {str(e)}'}), 500

# Rota para atualizar um usuário (autenticador é aplicado como middleware)
@api_usuarios.route(ini_rotas['update'], methods=['PUT'])
@autenticador
def update_user(usuario_id):
    current_user = get_jwt_identity()  
    
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    
    if not nome or not email or not senha:
        return jsonify({'message': 'Dados incompletos. Todos os campos são obrigatórios.'}), 400
    
    try:
        g.db.atualizar_usuario(usuario_id, nome, email, senha)
        return jsonify({'message': f'Usuário ID {usuario_id} atualizado com sucesso.'}), 200
    except Exception as e:
        return jsonify({'message': f'Erro ao atualizar usuário: {str(e)}'}), 500

# Rota para deletar um usuário (autenticador é aplicado como middleware)
@api_usuarios.route(ini_rotas['delete'], methods=['DELETE'])
@autenticador
def delete_user(usuario_id):
    current_user = get_jwt_identity()  
    try:
        g.db.deletar_usuario(usuario_id)
        return jsonify({'message': f'Usuário ID {usuario_id} deletado com sucesso.'}), 200
    except Exception as e:
        return jsonify({'message': f'Erro ao deletar usuário: {str(e)}'}), 500
