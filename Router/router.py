# app/router.py

import sys
sys.path.append(".")
from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
from Api._apiUsuarios import authenticate_user

main_blueprint = Blueprint('main', __name__, template_folder="./Templates")

# Middleware para verificar se o usuário está autenticado
def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'logado' not in session:
            return redirect(url_for('main.login'))
        return fn(*args, **kwargs)
    return wrapper

@main_blueprint.route('/')
def home():
    return render_template('Home/index.html')

@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if 'logado' in session:
        return redirect(url_for('main.painel'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('password')

        if not email or not senha:
            message = 'Email e senha são obrigatórios.'
            return render_template('Login/index.html', message=message)

        usuario = authenticate_user(email, senha)
        
        if not usuario:
            message = 'Credenciais inválidas. Falha na autenticação.'
            return render_template('Login/index.html', message=message)

        session['logado'] = {
            'status': True,
            'message': 'Autenticação bem-sucedida.',
            'usuario': usuario,
            'email': email,
        }
        return redirect(url_for('main.painel'))

    return render_template('Login/index.html')

@main_blueprint.route('/painel')
@login_required
def painel():
    return render_template('Painel/index.html', usuario=session['logado']['usuario'])

@main_blueprint.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('main.login'))
