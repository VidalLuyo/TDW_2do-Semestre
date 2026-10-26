"""Inicialización de Flask-SQLAlchemy y preparación de la base de datos."""

from flask_sqlalchemy import SQLAlchemy

# Instancia compartida por todos los modelos de la aplicación.
db = SQLAlchemy()


def init_db(app):
    """Vincula SQLAlchemy, crea las tablas y carga datos de demostración."""
    db.init_app(app)

    with app.app_context():
        # Importar los modelos permite que create_all detecte las tablas.
        from app import models  # noqa: F401
        from app.services.cliente_service import ClienteService

        db.create_all()
        ClienteService.sembrar_ejemplos()
