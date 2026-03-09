from flask import Flask
from .config import Config
from .extensions import db, migrate

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    return app

## flask db init - inicializar os migrates



## flask db migrate -m "initial tables" --- cria o migrate
## flask db upgrade ----- aplica no banco