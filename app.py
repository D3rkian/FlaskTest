import os
from flask import Flask
from extensions import db, migrate, lm
from models import Usuario

def create_app():
    app = Flask(__name__)

    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    caminho_db = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.getenv('DB_PATH'))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{caminho_db}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
    db.init_app(app)
    migrate.init_app(app, db)
    lm.init_app(app)

    
    lm.login_view = 'auth.login_page'

    
    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    
    @lm.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app

app = create_app()

@app.cli.command("novo-adm")
def novo_adm():
    
    
    username = input("Digite o nome de usuário para o admin: ")

    if Usuario.query.filter_by(username=username).first():
        print(f"Usuário '{username}' já existe.")
        return
    
    password = input("Digite a senha para o admin: ")

    


    
    admin_user = Usuario(username=username, role='admin')
    admin_user.set_password(password)

    
    db.session.add(admin_user)
    db.session.commit()
    print(f"Administrador '{username}' criado!")