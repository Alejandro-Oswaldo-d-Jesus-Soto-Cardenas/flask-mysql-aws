
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError

from app.database import db
from app.models.cliente import Cliente


def listar_clientes(busqueda="", page=1, per_page=10):
    consulta = select(Cliente)

    if busqueda:
        patron = f"%{busqueda}%"

        consulta = consulta.where(
            or_(
                Cliente.nombre.ilike(patron),
                Cliente.correo.ilike(patron),
                Cliente.telefono.ilike(patron),
            )
        )

    consulta = consulta.order_by(Cliente.id.desc())

    return db.paginate(
        consulta,
        page=page,
        per_page=per_page,
        max_per_page=50,
        error_out=False,
    )


def contar_clientes():
    consulta = select(func.count()).select_from(Cliente)
    return db.session.scalar(consulta) or 0


def obtener_cliente(cliente_id):
    return db.session.get(Cliente, cliente_id)


def crear_cliente(nombre, correo, telefono):
    cliente = Cliente(
        nombre=nombre.strip(),
        correo=correo.strip().lower(),
        telefono=telefono.strip() or None,
    )

    db.session.add(cliente)

    try:
        db.session.commit()
        return True, "Cliente registrado correctamente."

    except IntegrityError:
        db.session.rollback()
        return False, "Ese correo ya está registrado."


def actualizar_cliente(cliente, nombre, correo, telefono):
    cliente.nombre = nombre.strip()
    cliente.correo = correo.strip().lower()
    cliente.telefono = telefono.strip() or None

    try:
        db.session.commit()
        return True, "Cliente actualizado correctamente."

    except IntegrityError:
        db.session.rollback()
        return False, "Ese correo ya pertenece a otro cliente."


def eliminar_cliente(cliente):
    db.session.delete(cliente)
    db.session.commit()
