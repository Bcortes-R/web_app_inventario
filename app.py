# app.py
from flask import Flask
import config
from extensions import db, login_manager

# Importar Blueprints
from routes.inventario import inventario_bp
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.usuarios import usuarios_bp # type: ignore
from routes.asignaciones import asignaciones_bp 
from routes.mantenimientos import mantenimientos_bp 
from routes.parametros import parametros_bp

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.login"  # type: ignore

# Registrar rutas
app.register_blueprint(dashboard_bp)
app.register_blueprint(inventario_bp, url_prefix="/inventario")
app.register_blueprint(auth_bp)
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")  
app.register_blueprint(asignaciones_bp, url_prefix="/asignaciones")
app.register_blueprint(mantenimientos_bp, url_prefix="/mantenimientos")
app.register_blueprint(parametros_bp, url_prefix="/parametros")

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
