from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import Usuario
from extensions import db


from functools import wraps


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        if not current_user.is_authenticated or current_user.role != 'admin':
            
            flash('Acesso negado. Esta área é apenas para administradores.', 'error')
            return redirect(url_for('auth.home')) 
        return f(*args, **kwargs)
    return decorated_function

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





@auth_bp.route('/admin/usuarios')
@admin_required 
def lista_usuarios():
    usuarios = Usuario.query.all()
    return render_template('admin/usuarios_lista.html', usuarios=usuarios)


@auth_bp.route('/admin/usuarios/update/<int:id>', methods=['GET', 'POST'])
@admin_required
def update_usuario(id):
    usuario = Usuario.query.get_or_404(id) 
    if request.method == 'POST':
        usuario.username = request.form.get('username')
        
        usuario.role = request.form.get('role')
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('auth.lista_usuarios'))
    return render_template('admin/usuarios_update.html', usuario=usuario)


@auth_bp.route('/admin/usuarios/delete/<int:id>')
@admin_required
def delete_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    
    if usuario.id == current_user.id:
        flash('Você não pode excluir sua própria conta de administrador.', 'error')
        return redirect(url_for('auth.lista_usuarios'))

    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('auth.lista_usuarios'))