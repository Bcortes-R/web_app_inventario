# routes/dashboard.py
from flask import Blueprint, render_template
from flask_login import login_required
from extensions import db
from database.models import Equipo, Asignacion  
from sqlalchemy import func

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def home():
    # 1. KPIs Generales
    total_equipos = Equipo.query.count()
    total_mantenimiento = Equipo.query.filter_by(
        estado_operativo="mantenimiento"
    ).count()
    total_baja = Equipo.query.filter_by(estado_operativo="baja").count()

    # 2. GRÁFICO 1 (Pastel): Estado Operativo
    datos_estado = (
        db.session.query(Equipo.estado_operativo, func.count(Equipo.id_equipo)) # type: ignore
        .group_by(Equipo.estado_operativo)
        .all()
    )

    labels_estado = [e[0] for e in datos_estado]
    values_estado = [e[1] for e in datos_estado]

    # 3. GRÁFICO 2 (Barras): Equipos por Marca
    datos_marca = (
        db.session.query(Equipo.marca, func.count(Equipo.id_equipo)) # type: ignore
        .group_by(Equipo.marca)
        .all()
    )

    labels_marca = [m[0] for m in datos_marca]
    values_marca = [m[1] for m in datos_marca]

    # 4. 🌟 NUEVO GRÁFICO 3 (Línea): Asignaciones por Fecha (Evolución) 🌟
    # Agrupamos por fecha de asignación y contamos cuántas se hicieron ese día
    datos_cron = (
        db.session.query(Asignacion.fecha_asign, func.count(Asignacion.id_asignacion)) # type: ignore
        .group_by(Asignacion.fecha_asign)
        .order_by(Asignacion.fecha_asign)
        .all()
    )

    # Convertimos las fechas a string para que Chart.js las entienda
    labels_fecha = [d[0].strftime("%Y-%m-%d") for d in datos_cron]
    values_fecha = [d[1] for d in datos_cron]

    return render_template(
        "dashboard.html",
        total=total_equipos,
        mant=total_mantenimiento,
        baja=total_baja,
        labels_estado=labels_estado,
        values_estado=values_estado,
        labels_marca=labels_marca,
        values_marca=values_marca,
        labels_fecha=labels_fecha,  # <--- Enviamos datos nuevos
        values_fecha=values_fecha,
    ) 