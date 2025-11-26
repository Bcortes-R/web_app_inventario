from extensions import db
from flask_login import UserMixin
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash


# --- MODELO DE USUARIOS (Login) ---
class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario"
    id_usuario = db.Column(db.Integer, primary_key=True)
    doc_ident = db.Column(db.String(40), unique=True, nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True)
    rol = db.Column(db.String(60))  # 'admin' o 'usuario'
    password_hash = db.Column(db.String(255))
    id_dpto = db.Column(db.Integer, db.ForeignKey("departamento.id_dpto"))
    
    def __init__(
        self,
        doc_ident=None,
        nombre=None,
        email=None,
        rol=None,
        password_hash=None,
        id_dpto=None,
        **kwargs,
    ):
        self.doc_ident = doc_ident
        self.nombre = nombre
        self.email = email
        self.rol = rol
        self.password_hash = password_hash
        self.id_dpto = id_dpto
        super().__init__(**kwargs)

    def get_id(self):
        return str(self.id_usuario)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Si el usuario no tiene contraseña guardada, la validación falla automáticamente
        if not self.password_hash:
            return False
        # Si hay contraseña, procedemos a verificarla
        return check_password_hash(self.password_hash, password)


# --- MODELOS DE INVENTARIO ---
class Departamento(db.Model):
    __tablename__ = "departamento"
    id_dpto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    equipos = db.relationship("Equipo", backref="departamento", lazy=True)

# --- MODELO DE CATEGORÍA DE EQUIPOS ---
class CategoriaEquipo(db.Model):
    __tablename__ = "categoria_equipo"
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    equipos = db.relationship("Equipo", backref="categoria", lazy=True)

# --- MODELO DE EQUIPOS ---
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

    # Constructor personalizado
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
    # 1. Asignamos manualmente los valores a la instancia (self)
        self.serial = serial
        self.modelo = modelo
        self.marca = marca
        self.estado_operativo = estado_operativo
        self.fecha_compra = fecha_compra
        self.id_categoria = id_categoria
        self.id_dpto = id_dpto

    # 2. Llamamos al constructor padre solo con el resto de argumentos (**kwargs)
        super().__init__(**kwargs)   
    
# --- MODELO DE ASIGNACIONES --- 
class Asignacion(db.Model):
    __tablename__ = "asignacion"
    id_asignacion = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(
        db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_equipo = db.Column(db.Integer, db.ForeignKey("equipo.id_equipo"), nullable=False)
    fecha_asign = db.Column(db.Date, nullable=False, default=date.today)
    fecha_devol = db.Column(
        db.Date, nullable=True
    )  # Si es NULL, está asignado actualmente
    observaciones = db.Column(db.Text)

    # Relaciones para acceder fácil (asignacion.usuario.nombre)
    usuario = db.relationship("Usuario", backref="asignaciones")
    equipo = db.relationship("Equipo", backref="asignaciones")

    def __init__(self, id_usuario, id_equipo, fecha_asign=None, observaciones=None):
        self.id_usuario = id_usuario
        self.id_equipo = id_equipo
        self.fecha_asign = fecha_asign or date.today()
        self.observaciones = observaciones
        
# ----- MODELO TÉCNICO ----
class Tecnico(db.Model):
    __tablename__ = "tecnico"
    id_tecnico = db.Column(db.Integer, primary_key=True)
    doc_iden = db.Column(db.String(40), unique=True, nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    especialidad = db.Column(db.String(120))
    telefono = db.Column(db.String(30))
    email = db.Column(db.String(120), unique=True)

    mantenimientos = db.relationship("Mantenimiento", backref="tecnico", lazy=True)

    def __init__(
        self,
        doc_iden=None,
        nombre=None,
        especialidad=None,
        telefono=None,
        email=None,
        **kwargs,
    ):
        self.doc_iden = doc_iden
        self.nombre = nombre
        self.especialidad = especialidad
        self.telefono = telefono
        self.email = email
        super().__init__(**kwargs)

# ---- MODELO MANTENIMIENTO ------
class Mantenimiento(db.Model):
    __tablename__ = "mantenimiento"
    id_mnto = db.Column(db.Integer, primary_key=True)
    id_equipo = db.Column(db.Integer, db.ForeignKey("equipo.id_equipo"), nullable=False)
    id_tecnico = db.Column(
        db.Integer, db.ForeignKey("tecnico.id_tecnico"), nullable=True
    )
    fecha_mnto = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.String(60))  # 'preventivo', 'correctivo'
    descripcion = db.Column(db.Text)

    # Relación con Equipo
    equipo = db.relationship("Equipo", backref="mantenimientos")

    def __init__(
        self,
        id_equipo,
        id_tecnico=None,
        fecha_mnto=None,
        tipo=None,
        descripcion=None,
        **kwargs,
    ):
        self.id_equipo = id_equipo
        self.id_tecnico = id_tecnico
        self.fecha_mnto = fecha_mnto
        self.tipo = tipo
        self.descripcion = descripcion
        super().__init__(**kwargs)