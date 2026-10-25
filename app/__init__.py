from dotenv import load_dotenv

load_dotenv()

from flask import Flask, redirect, url_for
from app.config import Config
from app.database import db
from app.routes.clientes import clientes_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(clientes_bp)

    @app.get("/")
    def inicio():
        return redirect(url_for("clientes.index"))

    return app