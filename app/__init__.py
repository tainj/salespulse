from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Регистрируем маршруты
    from .routes.web import bp
    app.register_blueprint(bp)

    return app