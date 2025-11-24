# config.py
import urllib.parse

# 1. Define tus credenciales aquí
DB_USER = "root"  # Ej: 'root'
DB_PASS = "P@ssw0rd"  # Pon aquí tu contraseña real CON los símbolos
DB_HOST = "localhost"  # Generalmente es 'localhost' o '127.0.0.1'
DB_NAME = "inventario"

# 2. Codificamos la contraseña para que los símbolos como '@' no rompan la conexión
encoded_password = urllib.parse.quote_plus(DB_PASS)

# 3. Construimos la URI de conexión de forma segura
SQLALCHEMY_DATABASE_URI = (
    f"mysql://{DB_USER}:{encoded_password}@{DB_HOST}:3306/{DB_NAME}"
)

# Otras configuraciones
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "clave_secreta_segura"
