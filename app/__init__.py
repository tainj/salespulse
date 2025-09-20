from flask import Flask

from app.db.db import init_db


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = 'your-super-secret-key-here-1234567890'
    init_db()

    # Регистрируем маршруты
    from .routes.web import bp
    app.register_blueprint(bp)

    return app