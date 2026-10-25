from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.cliente_service import (
    listar_clientes,
    obtener_cliente,
    crear_cliente,
    actualizar_cliente,
    eliminar_cliente,
)

clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes")


@clientes_bp.get("/")
def index():
    clientes = listar_clientes()
    return render_template("clientes/index.html", clientes=clientes)


@clientes_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip()
        telefono = request.form.get("telefono", "").strip()

        if not nombre or not correo:
            flash("El nombre y el correo son obligatorios.", "error")
            return render_template("clientes/form.html", cliente=None)

        ok, mensaje = crear_cliente(nombre, correo, telefono)
        flash(mensaje, "success" if ok else "error")

        if ok:
            return redirect(url_for("clientes.index"))

    return render_template("clientes/form.html", cliente=None)


@clientes_bp.route("/editar/<int:cliente_id>", methods=["GET", "POST"])
def editar(cliente_id):
    cliente = obtener_cliente(cliente_id)

    if cliente is None:
        flash("El cliente no existe.", "error")
        return redirect(url_for("clientes.index"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip()
        telefono = request.form.get("telefono", "").strip()

        if not nombre or not correo:
            flash("El nombre y el correo son obligatorios.", "error")
        else:
            ok, mensaje = actualizar_cliente(
                cliente, nombre, correo, telefono
            )
            flash(mensaje, "success" if ok else "error")

            if ok:
                return redirect(url_for("clientes.index"))

    return render_template("clientes/form.html", cliente=cliente)


@clientes_bp.post("/eliminar/<int:cliente_id>")
def eliminar(cliente_id):
    cliente = obtener_cliente(cliente_id)

    if cliente is None:
        flash("El cliente no existe.", "error")
    else:
        eliminar_cliente(cliente)
        flash("Cliente eliminado correctamente.", "success")

    return redirect(url_for("clientes.index"))