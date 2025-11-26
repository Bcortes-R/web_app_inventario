# routes/parametros.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from extensions import db
from database.models import Departamento, CategoriaEquipo
from functools import wraps

parametros_bp = Blueprint("parametros", __name__)


# --- Decorador de Admin (Copiado para proteger este módulo) ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != "admin":
            abort(403)
        return f(*args, **kwargs)

    return decorated_function



# GESTIÓN DE DEPARTAMENTOS



@parametros_bp.route("/departamentos")
@login_required
@admin_required
def listar_departamentos():
    dptos = Departamento.query.order_by(Departamento.nombre).all()
    return render_template("parametros/departamentos_lista.html", departamentos=dptos)


@parametros_bp.route("/departamentos/crear", methods=["GET", "POST"])
@login_required
@admin_required
def crear_departamento():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        if Departamento.query.filter_by(nombre=nombre).first():
            flash("El departamento ya existe.", "error")
        else:
            nuevo = Departamento(nombre=nombre) # type: ignore
            db.session.add(nuevo)
            db.session.commit()
            flash("Departamento creado.", "success")
            return redirect(url_for("parametros.listar_departamentos"))
    return render_template(
        "parametros/departamento_form.html", titulo="Crear Departamento"
    )


@parametros_bp.route("/departamentos/editar/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def editar_departamento(id):
    dpto = Departamento.query.get_or_404(id)
    if request.method == "POST":
        dpto.nombre = request.form.get("nombre")
        db.session.commit()
        flash("Departamento actualizado.", "success")
        return redirect(url_for("parametros.listar_departamentos"))
    return render_template(
        "parametros/departamento_form.html", titulo="Editar Departamento", dpto=dpto
    )


@parametros_bp.route("/departamentos/eliminar/<int:id>", methods=["POST"])
@login_required
@admin_required
def eliminar_departamento(id):
    dpto = Departamento.query.get_or_404(id)
    try:
        db.session.delete(dpto)
        db.session.commit()
        flash("Departamento eliminado.", "success")
    except Exception:
        db.session.rollback()
        flash(
            "No se puede eliminar: Hay usuarios o equipos vinculados a este departamento.",
            "error",
        )
    return redirect(url_for("parametros.listar_departamentos"))



# GESTIÓN DE CATEGORÍAS



@parametros_bp.route("/categorias")
@login_required
@admin_required
def listar_categorias():
    cats = CategoriaEquipo.query.order_by(CategoriaEquipo.nombre).all()
    return render_template("parametros/categorias_lista.html", categorias=cats)


@parametros_bp.route("/categorias/crear", methods=["GET", "POST"])
@login_required
@admin_required
def crear_categoria():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        if CategoriaEquipo.query.filter_by(nombre=nombre).first():
            flash("La categoría ya existe.", "error")
        else:
            nuevo = CategoriaEquipo(nombre=nombre) # type: ignore
            db.session.add(nuevo)
            db.session.commit()
            flash("Categoría creada.", "success")
            return redirect(url_for("parametros.listar_categorias"))
    return render_template("parametros/categoria_form.html", titulo="Crear Categoría")


@parametros_bp.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def editar_categoria(id):
    cat = CategoriaEquipo.query.get_or_404(id)
    if request.method == "POST":
        cat.nombre = request.form.get("nombre")
        db.session.commit()
        flash("Categoría actualizada.", "success")
        return redirect(url_for("parametros.listar_categorias"))
    return render_template(
        "parametros/categoria_form.html", titulo="Editar Categoría", cat=cat
    )


@parametros_bp.route("/categorias/eliminar/<int:id>", methods=["POST"])
@login_required
@admin_required
def eliminar_categoria(id):
    cat = CategoriaEquipo.query.get_or_404(id)
    try:
        db.session.delete(cat)
        db.session.commit()
        flash("Categoría eliminada.", "success")
    except Exception:
        db.session.rollback()
        flash("No se puede eliminar: Hay equipos vinculados a esta categoría.", "error")
    return redirect(url_for("parametros.listar_categorias"))
