from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from .db_config import DBConfig, db
from flask_migrate import Migrate
from flask_login import LoginManager
from .models import User
from flask_restx import Api
from .controllers.user_controllers import api as users_ns


#db = SQLAlchemy()
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
    api.add_namespace(users_ns, path='/users')
    # api.add_namespace(home_ns, path='/posts')

    return app


app = create_app()