# app.py
from flask import Flask
import config
from extensions import db  # 🟢 Importamos db desde extensions

# 1. Inicialización de Flask
app = Flask(__name__)
app.config.from_object(config)

# 2. Inicializar la base de datos con la app
db.init_app(app)

# 3. Importar Modelos (solo para asegurarse de que SQLAlchemy los conozca)
#    Esto ya no causa error porque models.py importa de extensions, no de app.
from database import models #noqa

# 4. Registrar Rutas
#    Esto ya no causa error porque routes importa de extensions, no de app.
from routes.inventario import inventario_bp #noqa

app.register_blueprint(inventario_bp)

# 5. Ejecución
if __name__ == "__main__":
    app.run(debug=True)
