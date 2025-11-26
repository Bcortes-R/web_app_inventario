from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from database.models import Asignacion, Equipo, Usuario
from datetime import date

asignaciones_bp = Blueprint("asignaciones", __name__)


# 1. LISTAR ASIGNACIONES ACTIVAS
@asignaciones_bp.route("/")
@login_required
def listar_asignaciones():
    # USAMOS .is_(None) PARA EVITAR ADVERTENCIAS
    asignaciones_activas = Asignacion.query.filter(
        Asignacion.fecha_devol.is_(None)
    ).all()
    return render_template("asignaciones/lista.html", asignaciones=asignaciones_activas)


# 2. NUEVA ASIGNACIÓN
@asignaciones_bp.route("/nueva", methods=["GET", "POST"])
@login_required
def nueva_asignacion():
    if request.method == "POST":
        try:
            id_equipo = request.form.get("equipo")
            id_usuario = request.form.get("usuario")
            obs = request.form.get("observaciones")

            # Validar existencia del equipo (Solución Error 1)
            equipo = Equipo.query.get(id_equipo)
            if not equipo:
                flash("Error: Equipo no encontrado.", "error")
                return redirect(url_for("asignaciones.nueva_asignacion"))

            # Validar estado
            if equipo.estado_operativo != "operativo":
                flash("Error: Solo se pueden asignar equipos operativos.", "error")
                return redirect(url_for("asignaciones.nueva_asignacion"))

            # Validar duplicados (Solución Error 2 - .is_(None))
            asignado = Asignacion.query.filter(
                Asignacion.id_equipo == id_equipo, Asignacion.fecha_devol.is_(None) # type: ignore
            ).first()

            if asignado:
                flash("Error: Este equipo ya está prestado.", "error")
                return redirect(url_for("asignaciones.nueva_asignacion"))

            # Crear asignación
            nueva = Asignacion(
                id_usuario=id_usuario, id_equipo=id_equipo, observaciones=obs
            )
            db.session.add(nueva)
            db.session.commit()

            flash("Equipo asignado correctamente.", "success")
            return redirect(url_for("asignaciones.listar_asignaciones"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}", "error")

    # Cargar datos para el formulario
    # USAMOS .is_(None) EN LA SUBQUERY TAMBIÉN
    subquery_asignados = db.session.query(Asignacion.id_equipo).filter(  # type: ignore
        Asignacion.fecha_devol.is_(None)
    )

    equipos_disponibles = Equipo.query.filter(
        Equipo.estado_operativo == "operativo",
        ~Equipo.id_equipo.in_(subquery_asignados),
    ).all()

    usuarios = Usuario.query.all()

    return render_template(
        "asignaciones/crear.html", equipos=equipos_disponibles, usuarios=usuarios
    )


# 3. DEVOLVER EQUIPO
@asignaciones_bp.route("/devolver/<int:id_asignacion>", methods=["POST"])
@login_required
def devolver_equipo(id_asignacion):
    asignacion = Asignacion.query.get_or_404(id_asignacion)
    asignacion.fecha_devol = date.today()
    db.session.commit()
    flash("Equipo devuelto al inventario.", "success")
    return redirect(url_for("asignaciones.listar_asignaciones"))
