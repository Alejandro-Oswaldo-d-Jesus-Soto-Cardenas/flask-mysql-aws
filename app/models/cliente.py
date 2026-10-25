from app.database import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), nullable=False, unique=True)
    telefono = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"<Cliente {self.nombre}>"