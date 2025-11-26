from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import login_manager
from database.models import Usuario

auth_bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Si ya está logueado, lo mandamos al dashboard
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Usuario.query.filter_by(email=email).first()

        # Verificamos credenciales
        if user and user.check_password(password):
            login_user(user)
            # 🌟 AQUÍ ESTÁ EL CAMBIO: Mensaje de éxito 🌟
            flash(f"¡Bienvenido de nuevo, {user.nombre}!", "success")
            return redirect(url_for("dashboard.home"))
        else:
            # Mensaje de error (este ya lo tenías, pero ahora se verá con SweetAlert)
            flash("Correo o contraseña incorrectos. Intenta de nuevo.", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    # 🌟 Mensaje de despedida 🌟
    flash("Has cerrado sesión correctamente. ¡Hasta pronto!", "success")
    return redirect(url_for("auth.login"))
