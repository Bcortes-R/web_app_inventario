from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from extensions import db
from database.models import Equipo, CategoriaEquipo, Departamento
from datetime import date

inventario_bp = Blueprint("inventario", __name__)


def _procesar_fecha(fecha_str):
    if fecha_str and fecha_str.strip():
        return date.fromisoformat(fecha_str)
    return None


@inventario_bp.route("/")
@login_required
def listar_equipos():
    equipos = Equipo.query.order_by(Equipo.serial).all()
    return render_template("inventario.html", equipos=equipos)


@inventario_bp.route("/crear", methods=["GET", "POST"])
@login_required
def crear_equipo():
    categorias = CategoriaEquipo.query.all()
    departamentos = Departamento.query.all()
    estados = ["operativo", "mantenimiento", "baja", "dañado", "otro"]

    if request.method == "POST":
        try:
            nuevo = Equipo(
                serial=request.form.get("serial"),
                modelo=request.form.get("modelo"),
                marca=request.form.get("marca"),
                estado_operativo=request.form.get("estado"),
                fecha_compra=_procesar_fecha(request.form.get("fecha_compra")),
                id_categoria=request.form.get("categoria"),
                id_dpto=request.form.get("departamento") or None,
            )
            db.session.add(nuevo)
            db.session.commit()
            return redirect(url_for("inventario.listar_equipos"))
        except Exception as e:
            db.session.rollback()
            return render_template(
                "crear_equipo.html",
                categorias=categorias,
                departamentos=departamentos,
                estados=estados,
                error=str(e),
            )

    return render_template(
        "crear_equipo.html",
        categorias=categorias,
        departamentos=departamentos,
        estados=estados,
    )


@inventario_bp.route("/editar/<int:id_equipo>", methods=["GET", "POST"])
@login_required
def editar_equipo(id_equipo):
    equipo = Equipo.query.get_or_404(id_equipo)
    categorias = CategoriaEquipo.query.all()
    departamentos = Departamento.query.all()
    estados = ["operativo", "mantenimiento", "baja", "dañado", "otro"]

    if request.method == "POST":
        try:
            equipo.serial = request.form.get("serial")
            equipo.modelo = request.form.get("modelo")
            equipo.marca = request.form.get("marca")
            equipo.estado_operativo = request.form.get("estado")
            equipo.fecha_compra = _procesar_fecha(request.form.get("fecha_compra"))
            equipo.id_categoria = request.form.get("categoria")
            equipo.id_dpto = request.form.get("departamento") or None

            db.session.commit()
            return redirect(url_for("inventario.listar_equipos"))
        except Exception as e:
            db.session.rollback()
            return render_template(
                "editar_equipo.html",
                equipo=equipo,
                categorias=categorias,
                departamentos=departamentos,
                estados=estados,
                error=str(e),
            )

    return render_template(
        "editar_equipo.html",
        equipo=equipo,
        categorias=categorias,
        departamentos=departamentos,
        estados=estados,
    )


@inventario_bp.route("/eliminar/<int:id_equipo>", methods=["POST"])
@login_required
def eliminar_equipo(id_equipo):
    equipo = Equipo.query.get_or_404(id_equipo)
    db.session.delete(equipo)
    db.session.commit()
    return redirect(url_for("inventario.listar_equipos"))
