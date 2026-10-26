"""Modelo de datos para los clientes de la demo."""

from app.database import db


class Cliente(db.Model):
    """Representa a un cliente almacenado en SQLite."""

    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), nullable=False, unique=True, index=True)
    telefono = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        """Devuelve una representación útil al depurar."""
        return f"<Cliente {self.nombre}: {self.correo}>"
