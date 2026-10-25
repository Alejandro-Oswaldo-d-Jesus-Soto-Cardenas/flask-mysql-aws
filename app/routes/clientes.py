
import re

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app.services.cliente_service import (
    listar_clientes,
    contar_clientes,
    obtener_cliente,
    crear_cliente,
    actualizar_cliente,
    eliminar_cliente,
)

clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes")


def validar_datos(nombre, correo, telefono):
    if len(nombre) < 2:
        return "El nombre debe tener al menos 2 caracteres."

    if len(nombre) > 100:
        return "El nombre no puede superar los 100 caracteres."

    if not correo or len(correo) > 120:
        return "Ingresa un correo válido de máximo 120 caracteres."

    patron_correo = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.fullmatch(patron_correo, correo):
        return "El formato del correo electrónico no es válido."

    if telefono and not re.fullmatch(r"[0-9+()\-\s]{7,20}", telefono):
        return "El teléfono debe tener entre 7 y 20 caracteres válidos."

    return None


@clientes_bp.get("/")
def index():
    busqueda = request.args.get("q", "").strip()
    pagina = request.args.get("page", 1, type=int) or 1
    pagina = max(pagina, 1)

    clientes = listar_clientes(
        busqueda=busqueda,
        page=pagina,
        per_page=10,
    )

    return render_template(
        "clientes/index.html",
        clientes=clientes,
        busqueda=busqueda,
        total_clientes=contar_clientes(),
    )


@clientes_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip()
        telefono = request.form.get("telefono", "").strip()

        error = validar_datos(nombre, correo, telefono)

        if error:
            flash(error, "error")
        else:
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

        error = validar_datos(nombre, correo, telefono)

        if error:
            flash(error, "error")
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
