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