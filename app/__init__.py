from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.models import anomaly, inventory, item, kitchen, log, menu_item, menu, school, warehouse

    return app
