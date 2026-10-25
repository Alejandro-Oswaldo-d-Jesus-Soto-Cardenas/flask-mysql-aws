from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.database import db
from app.models.cliente import Cliente


def listar_clientes():
    return db.session.execute(
        select(Cliente).order_by(Cliente.id.desc())
    ).scalars().all()


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