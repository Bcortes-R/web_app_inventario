# crear_tecnico.py
from app import app
from extensions import db
from database.models import Tecnico

with app.app_context():
    t = Tecnico(
        doc_iden="TEC-001",
        nombre="Juan Técnico",
        especialidad="Hardware",
        email="juan@soporte.com",
    )
    db.session.add(t)
    db.session.commit()
    print("Técnico creado.")
