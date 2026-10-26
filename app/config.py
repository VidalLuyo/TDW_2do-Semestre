"""Configuración de la aplicación basada en variables de entorno."""

import os

from dotenv import load_dotenv

# Carga el archivo .env cuando exista, sin fallar si aún no fue creado.
load_dotenv()


class Config:
    """Valores de configuración usados por la fábrica de la aplicación."""

    SECRET_KEY = os.getenv("SECRET_KEY", "clave-demo-solo-para-desarrollo")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///clientes.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
