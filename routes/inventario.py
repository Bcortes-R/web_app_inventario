# routes/inventario.py
from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db  # 🟢 Importamos desde extensions, NO desde app
from database.models import Equipo, CategoriaEquipo, Departamento
from datetime import date

inventario_bp = Blueprint("inventario", __name__)

# ... (El resto del código de las rutas LISTAR, CREAR, EDITAR, ELIMINAR sigue IGUAL) ...
# ... (Solo asegúrate de cambiar la línea 2 'from app import db' por la nueva) ...


# Función auxiliar
def _procesar_fecha(fecha_str):
    if fecha_str and fecha_str.strip():
        return date.fromisoformat(fecha_str)
    return None


@inventario_bp.route("/")
def listar_equipos():
    try:
        equipos = Equipo.query.order_by(Equipo.serial).all()
        return render_template("inventario.html", equipos=equipos)
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return f"Error al cargar el inventario: {e}", 500


@inventario_bp.route("/crear", methods=["GET", "POST"])
def crear_equipo():
    categorias = CategoriaEquipo.query.all()
    departamentos = Departamento.query.all()
    estados = ["operativo", "mantenimiento", "baja", "dañado", "otro"]

    if request.method == "POST":
        try:
            fecha_compra_obj = _procesar_fecha(request.form.get("fecha_compra"))
            nuevo_equipo = Equipo(
                serial=request.form.get("serial"),
                modelo=request.form.get("modelo"),
                marca=request.form.get("marca"),
                estado_operativo=request.form.get("estado"),
                fecha_compra=fecha_compra_obj,
                id_categoria=request.form.get("categoria"),
                id_dpto=request.form.get("departamento") or None,
            )
            db.session.add(nuevo_equipo)
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
def editar_equipo(id_equipo):
    equipo = Equipo.query.get_or_404(id_equipo)
    categorias = CategoriaEquipo.query.all()
    departamentos = Departamento.query.all()
    estados = ["operativo", "mantenimiento", "baja", "dañado", "otro"]

    if request.method == "POST":
        try:
            fecha_compra_obj = _procesar_fecha(request.form.get("fecha_compra"))
            equipo.serial = request.form.get("serial")
            equipo.modelo = request.form.get("modelo")
            equipo.marca = request.form.get("marca")
            equipo.estado_operativo = request.form.get("estado")
            equipo.fecha_compra = fecha_compra_obj
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
def eliminar_equipo(id_equipo):
    equipo_a_eliminar = Equipo.query.get_or_404(id_equipo)
    db.session.delete(equipo_a_eliminar)
    db.session.commit()
    return redirect(url_for("inventario.listar_equipos"))
