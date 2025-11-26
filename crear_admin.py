# crear_admin.py
from app import app
from extensions import db
from database.models import Usuario

# Bloque necesario para acceder a la BD fuera del servidor web
with app.app_context():
    # 1. Borrar tablas y crearlas de nuevo (OPCIONAL - SOLO SI TIENES PROBLEMAS DE ESTRUCTURA)
    # db.drop_all()
    # db.create_all()

    # 2. Verificar si ya existe el admin para no duplicarlo
    admin_existente = Usuario.query.filter_by(email="admin@empresa.com").first()

    if not admin_existente:
        # Crear el objeto Usuario
        u = Usuario(
            doc_ident="1001",
            nombre="Administrador",
            email="admin@empresa.com",
            rol="admin",  # Importante para los permisos
        )

        # Encriptar la contraseña
        u.set_password("123456")

        # Guardar en BD
        db.session.add(u)
        db.session.commit()
        print("✅ ¡Usuario Administrador creado exitosamente!")
        print("   Email: admin@empresa.com")
        print("   Pass:  123456")
    else:
        print("ℹ️ El usuario administrador ya existe. No se hicieron cambios.")
