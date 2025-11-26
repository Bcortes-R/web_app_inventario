from flask import Blueprint, render_template
from flask_login import login_required, current_user
from database.models import Equipo

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def home():
    total_equipos = Equipo.query.count()
    total_mantenimiento = Equipo.query.filter_by(
        estado_operativo="mantenimiento"
    ).count()
    total_baja = Equipo.query.filter_by(estado_operativo="baja").count()

    return render_template(
        "dashboard.html", total=total_equipos, mant=total_mantenimiento, baja=total_baja
    )
