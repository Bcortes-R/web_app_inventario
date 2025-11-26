from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from extensions import db
from functools import wraps

# 🟢 IMPORTANTE: Importamos Usuario desde models.py
# Ya no escribimos "class Usuario..." aquí, solo lo traemos.
from database.models import Usuario

usuarios_bp = Blueprint("usuarios", __name__)


# --- DECORADOR PERSONALIZADO: Solo Admins ---
# Protege las rutas para que solo el rol 'admin' pueda entrar
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != "admin":
            abort(403)  # Error 403: Acceso Prohibido
        return f(*args, **kwargs)

    return decorated_function


# 1. LISTAR USUARIOS
@usuarios_bp.route("/")
@login_required
@admin_required
def listar_usuarios():
    # Filtramos para no mostrar al usuario actual en la lista (para no auto-borrarse)
    usuarios = Usuario.query.filter(Usuario.id_usuario != current_user.id_usuario).all()
    return render_template("usuarios/lista_usuarios.html", usuarios=usuarios)


# 2. CREAR USUARIO
@usuarios_bp.route("/crear", methods=["GET", "POST"])
@login_required
@admin_required
def crear_usuario():
    if request.method == "POST":
        try:
            doc = request.form.get("doc_ident")
            email = request.form.get("email")

            # Validar si ya existe el documento o el correo
            if Usuario.query.filter(
                (Usuario.doc_ident == doc) | (Usuario.email == email)
            ).first():
                flash("Error: El documento o email ya están registrados.", "error")
                return redirect(url_for("usuarios.crear_usuario"))

            # Creamos el objeto usando la clase importada
            nuevo_usuario = Usuario(
                doc_ident=doc,
                nombre=request.form.get("nombre"),
                email=email,
                rol=request.form.get("rol"),
            )
            # Encriptamos la contraseña
            nuevo_usuario.set_password(request.form.get("password"))

            db.session.add(nuevo_usuario)
            db.session.commit()

            flash("Usuario creado exitosamente.", "success")
            return redirect(url_for("usuarios.listar_usuarios"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear usuario: {str(e)}", "error")

    return render_template("usuarios/crear_usuario.html")


# 3. ELIMINAR USUARIO
@usuarios_bp.route("/eliminar/<int:id_usuario>", methods=["POST"])
@login_required
@admin_required
def eliminar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuario eliminado.", "success")
    return redirect(url_for("usuarios.listar_usuarios"))
