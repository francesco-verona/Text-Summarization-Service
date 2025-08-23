from flask import Flask

def create_app():
    app = Flask(__name__)

    # registra il blueprint delle route
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
