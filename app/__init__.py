from flask import Flask

# why not make this a module?
def create_app():
    app = Flask(__name__)

    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
