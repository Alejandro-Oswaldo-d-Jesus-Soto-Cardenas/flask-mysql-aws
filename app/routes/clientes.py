
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
    """Valida los datos recibidos desde el formulario."""

    # Nombre: obligatorio, entre 2 y 100 caracteres.
    if not nombre:
        return "El nombre es obligatorio."

    if len(nombre) < 2:
        return "El nombre debe tener al menos 2 caracteres."

    if len(nombre) > 100:
        return "El nombre no puede superar los 100 caracteres."

    if not re.search(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", nombre):
        return "El nombre debe contener al menos una letra."

    # Correo: obligatorio, formato válido y máximo 120 caracteres.
    if not correo:
        return "El correo electrónico es obligatorio."

    if len(correo) > 120:
        return "El correo no puede superar los 120 caracteres."

    patron_correo = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.fullmatch(patron_correo, correo):
        return "Ingresa un correo electrónico válido."

    # Teléfono: opcional. Si se ingresa, debe ser válido.
    if telefono:
        if len(telefono) > 20:
            return "El teléfono no puede superar los 20 caracteres."

        if not re.fullmatch(r"[0-9+()\-\s]+", telefono):
            return "El teléfono contiene caracteres no permitidos."

        cantidad_digitos = sum(
            caracter.isdigit() for caracter in telefono
        )

        if not 7 <= cantidad_digitos <= 15:
            return "El teléfono debe contener entre 7 y 15 dígitos."

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
    form_data = {
        "nombre": "",
        "correo": "",
        "telefono": "",
    }

    if request.method == "POST":
        form_data = {
            "nombre": request.form.get("nombre", "").strip(),
            "correo": request.form.get("correo", "").strip(),
            "telefono": request.form.get("telefono", "").strip(),
        }

        error = validar_datos(
            form_data["nombre"],
            form_data["correo"],
            form_data["telefono"],
        )

        if error:
            flash(error, "error")
        else:
            ok, mensaje = crear_cliente(
                form_data["nombre"],
                form_data["correo"],
                form_data["telefono"],
            )

            flash(mensaje, "success" if ok else "error")

            if ok:
                return redirect(url_for("clientes.index"))

    return render_template(
        "clientes/form.html",
        cliente=None,
        form_data=form_data,
    )


@clientes_bp.route("/editar/<int:cliente_id>", methods=["GET", "POST"])
def editar(cliente_id):
    cliente = obtener_cliente(cliente_id)

    if cliente is None:
        flash("El cliente no existe.", "error")
        return redirect(url_for("clientes.index"))

    form_data = {
        "nombre": cliente.nombre or "",
        "correo": cliente.correo or "",
        "telefono": cliente.telefono or "",
    }

    if request.method == "POST":
        form_data = {
            "nombre": request.form.get("nombre", "").strip(),
            "correo": request.form.get("correo", "").strip(),
            "telefono": request.form.get("telefono", "").strip(),
        }

        error = validar_datos(
            form_data["nombre"],
            form_data["correo"],
            form_data["telefono"],
        )

        if error:
            flash(error, "error")
        else:
            ok, mensaje = actualizar_cliente(
                cliente,
                form_data["nombre"],
                form_data["correo"],
                form_data["telefono"],
            )

            flash(mensaje, "success" if ok else "error")

            if ok:
                return redirect(url_for("clientes.index"))

    return render_template(
        "clientes/form.html",
        cliente=cliente,
        form_data=form_data,
    )


@clientes_bp.post("/eliminar/<int:cliente_id>")
def eliminar(cliente_id):
    cliente = obtener_cliente(cliente_id)

    if cliente is None:
        flash("El cliente no existe.", "error")
    else:
        eliminar_cliente(cliente)
        flash("Cliente eliminado correctamente.", "success")

    return redirect(url_for("clientes.index"))
