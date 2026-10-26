"""Lógica de negocio, validaciones y consultas de clientes."""

import re

from sqlalchemy.exc import IntegrityError

from app.database import db
from app.models import Cliente

CORREO_VALIDO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
TELEFONO_VALIDO = re.compile(r"^[0-9+()\s-]{7,30}$")


class ValidationError(Exception):
    """Agrupa los mensajes de validación que debe mostrar la vista."""

    def __init__(self, errores):
        super().__init__("; ".join(errores))
        self.errores = errores


class ClienteService:
    """Centraliza las operaciones de clientes para mantener las rutas simples."""

    @staticmethod
    def listar():
        """Devuelve todos los clientes ordenados por nombre."""
        return Cliente.query.order_by(Cliente.nombre.asc()).all()

    @staticmethod
    def obtener(cliente_id):
        """Busca un cliente por su identificador o devuelve None."""
        return db.session.get(Cliente, cliente_id)

    @staticmethod
    def _limpiar(datos):
        """Normaliza los campos recibidos desde un formulario."""
        return {
            "nombre": " ".join(str(datos.get("nombre", "")).split()),
            "correo": str(datos.get("correo", "")).strip().lower(),
            "telefono": " ".join(str(datos.get("telefono", "")).split()),
        }

    @classmethod
    def _validar(cls, datos, cliente_id=None):
        """Valida los campos y lanza ValidationError si hay problemas."""
        errores = []

        if len(datos["nombre"]) < 2:
            errores.append("El nombre debe tener al menos 2 caracteres.")
        elif len(datos["nombre"]) > 100:
            errores.append("El nombre no puede superar los 100 caracteres.")

        if not datos["correo"]:
            errores.append("El correo es obligatorio.")
        elif not CORREO_VALIDO.match(datos["correo"]):
            errores.append("Ingresa un correo electrónico válido.")
        else:
            consulta = Cliente.query.filter(Cliente.correo == datos["correo"])
            if cliente_id is not None:
                consulta = consulta.filter(Cliente.id != cliente_id)
            if consulta.first() is not None:
                errores.append("El correo ya está registrado.")

        if not datos["telefono"]:
            errores.append("El teléfono es obligatorio.")
        elif not TELEFONO_VALIDO.match(datos["telefono"]):
            errores.append(
                "El teléfono debe tener entre 7 y 30 caracteres válidos."
            )

        if errores:
            raise ValidationError(errores)

    @classmethod
    def crear(cls, datos):
        """Valida y guarda un cliente nuevo en la base de datos."""
        limpios = cls._limpiar(datos)
        cls._validar(limpios)

        cliente = Cliente(**limpios)
        db.session.add(cliente)
        try:
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            raise ValidationError(
                ["El correo ya está registrado."]
            ) from error

        return cliente

    @classmethod
    def actualizar(cls, cliente, datos):
        """Valida y actualiza los datos de un cliente existente."""
        limpios = cls._limpiar(datos)
        cls._validar(limpios, cliente_id=cliente.id)

        cliente.nombre = limpios["nombre"]
        cliente.correo = limpios["correo"]
        cliente.telefono = limpios["telefono"]

        try:
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            raise ValidationError(
                ["El correo ya está registrado."]
            ) from error

        return cliente

    @classmethod
    def sembrar_ejemplos(cls):
        """Inserta tres clientes de ejemplo solo cuando la tabla está vacía."""
        if Cliente.query.count() > 0:
            return

        ejemplos = [
            Cliente(
                nombre="Ana Torres",
                correo="ana.torres@example.com",
                telefono="+51 987 654 321",
            ),
            Cliente(
                nombre="Carlos Ramos",
                correo="carlos.ramos@example.com",
                telefono="555-123-4567",
            ),
            Cliente(
                nombre="Lucía Mendoza",
                correo="lucia.mendoza@example.com",
                telefono="+51 912 345 678",
            ),
        ]

        db.session.add_all(ejemplos)
        db.session.commit()
