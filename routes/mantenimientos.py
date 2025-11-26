# routes/mantenimientos.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from database.models import Mantenimiento, Equipo, Tecnico
from datetime import date

mantenimientos_bp = Blueprint("mantenimientos", __name__)


# Función auxiliar fecha
def _procesar_fecha(fecha_str):
    if fecha_str and fecha_str.strip():
        return date.fromisoformat(fecha_str)
    return date.today()


# 1. LISTAR HISTORIAL
@mantenimientos_bp.route("/")
@login_required
def listar_mantenimientos():
    historial = Mantenimiento.query.order_by(Mantenimiento.fecha_mnto.desc()).all() # type: ignore
    return render_template("mantenimientos/lista.html", historial=historial)


# 2. REGISTRAR NUEVO MANTENIMIENTO
@mantenimientos_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_mantenimiento():
    if request.method == "POST":
        try:
            id_equipo = request.form.get("equipo")
            id_tecnico = request.form.get("tecnico") or None

            # Crear registro
            nuevo_mnto = Mantenimiento(
                id_equipo=id_equipo,
                id_tecnico=id_tecnico,
                fecha_mnto=_procesar_fecha(request.form.get("fecha")),
                tipo=request.form.get("tipo"),
                descripcion=request.form.get("descripcion"),
            )

            # 🤖 AUTOMATIZACIÓN: Cambiar estado del equipo a 'mantenimiento'
            equipo = Equipo.query.get(id_equipo)
            if equipo:
                equipo.estado_operativo = "mantenimiento"

            db.session.add(nuevo_mnto)
            db.session.commit()

            flash(
                "Mantenimiento registrado. El equipo ahora está en reparación.",
                "success",
            )
            return redirect(url_for("mantenimientos.listar_mantenimientos"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}", "error")

    # Cargar datos para el formulario
    equipos = Equipo.query.order_by(Equipo.serial).all()
    tecnicos = Tecnico.query.all()

    return render_template(
        "mantenimientos/crear.html", equipos=equipos, tecnicos=tecnicos
    )


# 3. FINALIZAR MANTENIMIENTO (Volver a Operativo)
@mantenimientos_bp.route("/finalizar/<int:id_equipo>", methods=["POST"])
@login_required
def finalizar_mantenimiento(id_equipo):
    try:
        equipo = Equipo.query.get_or_404(id_equipo)
        # Cambiamos el estado a operativo
        equipo.estado_operativo = "operativo"
        db.session.commit()
        flash(f"El equipo {equipo.serial} ha sido marcado como Operativo.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar estado: {e}", "error")

    return redirect(url_for("mantenimientos.listar_mantenimientos"))
