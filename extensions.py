from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inicializamos las extensiones aquí sin vincularlas a la app aún
db = SQLAlchemy()
login_manager = LoginManager()
