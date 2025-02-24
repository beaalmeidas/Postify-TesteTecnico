from flask import Flask
from .db_config import DBConfig, db
from flask_migrate import Migrate
from .models import User
from flask_login import LoginManager
from flask_restx import Api
from .controllers.user_controllers import users_ns
from .controllers.post_controllers import posts_ns
from .controllers.auth_controllers import auth_ns


login_manager = LoginManager()
migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    app.config.from_object(DBConfig)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    api = Api(app, title='Api Flask Postify', version='1.0', description='Api de rede social com python flask',prefix='/api')
    
    # ROTAS
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(posts_ns, path='/posts')
    api.add_namespace(auth_ns, path='/auth')

    return app


app = create_app()