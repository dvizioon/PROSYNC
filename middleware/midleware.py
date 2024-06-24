# middleware.py

import sys
from flask import g, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from Controller.usuarioController import ControllerUsuario

def connect_db(database_path):
 
    def middleware(app):
        @app.before_request
        def before_request():
            g.db = ControllerUsuario(database_path)
            g.db.conectar()

        @app.teardown_appcontext
        def teardown_request(exception=None):
            db = getattr(g, 'db', None)
            if db is not None:
                db.fechar_conexao()

        return app

    return middleware

def autenticador(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            g.current_user = current_user
        except Exception as e:
            return jsonify({"message": "Token de autenticação inválido."}), 401
        return fn(*args, **kwargs)

    return wrapper
