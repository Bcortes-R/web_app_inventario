from flask import Blueprint, render_template, request, redirect, url_for, send_file, flash
from flask_login import login_required
from extensions import db
from database.models import Equipo, CategoriaEquipo, Departamento
from datetime import date
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_  # Para el buscador (O esto O aquello)
import pandas as pd  # Para Excel
import io  # Para el archivo en memoria


inventario_bp = Blueprint("inventario", __name__)


def _procesar_fecha(fecha_str):
    if fecha_str and fecha_str.strip():
        return date.fromisoformat(fecha_str)
    return None


# 1. LISTAR EQUIPOS (Con Buscador)
@inventario_bp.route("/")
@login_required
def listar_equipos():
    # Obtener término de búsqueda si existe
    busqueda = request.args.get("q")
    query = Equipo.query

    if busqueda:
        # Filtramos si el texto coincide con Serial, Modelo O Marca
        search_term = f"%{busqueda}%"
        query = query.filter(
            or_(
                Equipo.serial.ilike(search_term), # type: ignore
                Equipo.modelo.ilike(search_term), # type: ignore
                Equipo.marca.ilike(search_term), # type: ignore
            )
        )

    equipos = query.order_by(Equipo.serial).all()
    return render_template("inventario.html", equipos=equipos)


# 2. EXPORTAR A EXCEL (Nueva Ruta)
@inventario_bp.route("/exportar")
@login_required
def exportar_excel():
    equipos = Equipo.query.all()

    # Crear lista de diccionarios
    data = []
    for e in equipos:
        data.append(
            {
                "ID": e.id_equipo,
                "Serial": e.serial,
                "Marca": e.marca,
                "Modelo": e.modelo,
                "Estado": e.estado_operativo,
                "Fecha Compra": e.fecha_compra,
                "Categoría": e.categoria.nombre if e.categoria else "",
                "Departamento": e.departamento.nombre if e.departamento else "",
            }
        )

    # Generar Excel en memoria
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Inventario")
    output.seek(0)

    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="Reporte_Inventario.xlsx",
    )


# 3. CREAR EQUIPO
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


# 4. EDITAR EQUIPO
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


# 5. ELIMINAR EQUIPO (Versión Blindada)
@inventario_bp.route("/eliminar/<int:id_equipo>", methods=["POST"])
@login_required
def eliminar_equipo(id_equipo):
    equipo = Equipo.query.get_or_404(id_equipo)

    try:
        db.session.delete(equipo)
        db.session.commit()
        flash("Equipo eliminado correctamente.", "success") 

    except IntegrityError:
        # Esto captura el error si el equipo tiene asignaciones o historial
        db.session.rollback()
        flash(
            '⛔ No se puede eliminar este equipo porque tiene asignaciones o mantenimientos asociados. Considere cambiar su estado a "De Baja".',
            "error",
        )

    except Exception as e:
        # Captura cualquier otro error inesperado
        db.session.rollback()
        flash(f"Error desconocido al eliminar: {str(e)}", "error")

    return redirect(url_for("inventario.listar_equipos"))