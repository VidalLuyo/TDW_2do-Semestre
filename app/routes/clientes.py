"""Rutas HTTP para listar, crear y editar clientes."""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.models import Cliente
from app.services.cliente_service import ClienteService, ValidationError

clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes")


@clientes_bp.get("/")
def index():
    """Muestra el listado de clientes registrados."""
    clientes = ClienteService.listar()
    return render_template("clientes/index.html", clientes=clientes)


@clientes_bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    """Muestra el formulario y procesa la creación de un cliente."""
    if request.method == "POST":
        try:
            ClienteService.crear(request.form)
            flash("Cliente creado correctamente.", "success")
            return redirect(url_for("clientes.index"))
        except ValidationError as error:
            for mensaje in error.errores:
                flash(mensaje, "error")

            # Conserva lo escrito para que el usuario corrija el formulario.
            cliente = Cliente(
                nombre=request.form.get("nombre", ""),
                correo=request.form.get("correo", ""),
                telefono=request.form.get("telefono", ""),
            )
            return (
                render_template(
                    "clientes/form.html", cliente=cliente, modo="crear"
                ),
                400,
            )

    return render_template("clientes/form.html", cliente=None, modo="crear")


@clientes_bp.route("/<int:cliente_id>/editar", methods=["GET", "POST"])
def editar(cliente_id):
    """Muestra el formulario y procesa la edición de un cliente existente."""
    cliente = ClienteService.obtener(cliente_id)
    if cliente is None:
        flash("El cliente solicitado no existe.", "error")
        return redirect(url_for("clientes.index"))

    if request.method == "POST":
        try:
            ClienteService.actualizar(cliente, request.form)
            flash("Cliente actualizado correctamente.", "success")
            return redirect(url_for("clientes.index"))
        except ValidationError as error:
            for mensaje in error.errores:
                flash(mensaje, "error")

            # Los cambios no se confirman: solo se muestran para corregirlos.
            cliente.nombre = request.form.get("nombre", "")
            cliente.correo = request.form.get("correo", "")
            cliente.telefono = request.form.get("telefono", "")
            return (
                render_template(
                    "clientes/form.html", cliente=cliente, modo="editar"
                ),
                400,
            )

    return render_template("clientes/form.html", cliente=cliente, modo="editar")
