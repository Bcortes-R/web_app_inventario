# config.py
import urllib.parse
import os

# 1. Configuración básica de la base de datos

DB_USER = "root"  # username de la base de datos'
DB_PASS = "P@ssw0rd"  # contraseña 
DB_HOST = "localhost"  # host de la base de datos
DB_NAME = "inventario" # nombre de la base de datos

#Codificación de contraseña para evitar errores con caracteres especiales (@, #, etc.)
encoded_password = urllib.parse.quote_plus(DB_PASS)

# URI de conexión
SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER}:{encoded_password}@{DB_HOST}:3306/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Clave secreta para sesiones y seguridad (Cámbiala por algo aleatorio)
SECRET_KEY = 'ElgatoConBotas123!'