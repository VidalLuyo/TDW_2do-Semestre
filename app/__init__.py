"""Fábrica de la aplicación Flask.

Concentra la creación de la app, la carga de configuración, la inicialización
de la base de datos y el registro de los blueprints.
"""

from pathlib import Path

from flask import Flask, redirect, url_for

from .config import Config
from .database import init_db


def create_app(config_object=Config):
    """Crea y configura una instancia de la aplicación Flask."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    # Asegura que SQLite pueda crear su archivo dentro de instance/.
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    # Importar aquí evita ciclos de importación durante el arranque.
    from .routes import clientes_bp

    app.register_blueprint(clientes_bp)
    init_db(app)

    @app.get("/")
    def inicio():
        """Redirige la raíz al listado principal de clientes."""
        return redirect(url_for("clientes.index"))

    return app
