from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # 👈 Importa o Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()  # 👈 Cria a instância do Migrate

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'chave-secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financas.db'

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # 👈 Conecta o Migrate com a app e o db

    login_manager.login_view = 'routes.login'

    from .routes import routes
    app.register_blueprint(routes)

    from .models import User  # Garante que os modelos estão importados

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
