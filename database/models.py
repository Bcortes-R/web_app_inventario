# database/models.py
from extensions import db  # 🟢 Importamos desde extensions, NO desde app
from flask_sqlalchemy import SQLAlchemy

# Ya no necesitamos el truco de Model = db.Model ni la reasignación rara.
# Heredamos directamente de db.Model


# 1. Modelo Departamento
class Departamento(db.Model):
    __tablename__ = "departamento"
    id_dpto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    equipos = db.relationship("Equipo", backref="departamento", lazy=True)


# 2. Modelo CategoriaEquipo
class CategoriaEquipo(db.Model):
    __tablename__ = "categoria_equipo"
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    equipos = db.relationship("Equipo", backref="categoria", lazy=True)


# 3. Modelo Equipo
class Equipo(db.Model):
    __tablename__ = "equipo"
    id_equipo = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(80), unique=True, nullable=False)
    modelo = db.Column(db.String(100))
    marca = db.Column(db.String(100))
    estado_operativo = db.Column(
        db.Enum("operativo", "mantenimiento", "baja", "dañado", "otro")
    )
    fecha_compra = db.Column(db.Date)

    id_categoria = db.Column(db.Integer, db.ForeignKey("categoria_equipo.id_categoria"))
    id_dpto = db.Column(db.Integer, db.ForeignKey("departamento.id_dpto"))

    def __init__(
        self,
        serial=None,
        modelo=None,
        marca=None,
        estado_operativo=None,
        fecha_compra=None,
        id_categoria=None,
        id_dpto=None,
        **kwargs,
    ):
        super().__init__(
            serial=serial,
            modelo=modelo,
            marca=marca,
            estado_operativo=estado_operativo,
            fecha_compra=fecha_compra,
            id_categoria=id_categoria,
            id_dpto=id_dpto,
            **kwargs,
        )

    def __repr__(self):
        return f"<Equipo {self.serial} - {self.marca} {self.modelo}>"
