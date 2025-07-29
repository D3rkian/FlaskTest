from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import Usuario
from extensions import db

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

@auth_bp.route('/')
def login_page():
    
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    return render_template('LoginRegistro.html')

@auth_bp.route('/registrar', methods=['POST'])
def registrar():
    username = request.form.get('username')
    password = request.form.get('password')

    if Usuario.query.filter_by(username=username).first():
        flash('Este nome de usuário já existe.', 'error')
        return redirect(url_for('auth.login_page'))

    novo_usuario = Usuario(username=username)
    novo_usuario.set_password(password)
    db.session.add(novo_usuario)
    db.session.commit()

    flash('Conta criada com sucesso! Faça o login.', 'success')
    return redirect(url_for('auth.login_page'))

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = Usuario.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)
        
        return redirect(url_for('auth.home'))
    else:
        flash('Usuário ou senha inválidos.', 'error')
        return redirect(url_for('auth.login_page'))


@auth_bp.route('/home')
@login_required
def home():
    return render_template('index.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'success')
    return redirect(url_for('auth.login_page'))