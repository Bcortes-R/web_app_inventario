```
# 🏢 Sistema de Gestión de Inventario (InvApp)

Una aplicación web completa para la gestión, control y seguimiento del ciclo de vida de activos tecnológicos (hardware, periféricos, etc.). Desarrollada en **Python (Flask)** y **MySQL**.

## 🚀 Características Principales

* **📊 Dashboard Interactivo:** Visualización de KPIs en tiempo real, gráficos de estado (Pastel), marcas (Barras) y evolución de asignaciones (Línea).
* **🔐 Seguridad y Roles:** Autenticación robusta, encriptación de contraseñas y roles de usuario (Administrador, Técnico, Usuario Estándar).
* **📋 Inventario Completo:** CRUD de equipos con búsqueda instantánea y filtros.
* **🤝 Gestión de Asignaciones:** Control de préstamos y devoluciones de equipos a empleados.
* **🛠️ Módulo de Mantenimiento:** Registro de fallas, asignación de técnicos y ciclo de reparación (cambio automático de estados).
* **📄 Reportes:** Exportación de inventario a **Excel** con un solo clic.
* **📱 Diseño Responsivo:** Interfaz moderna adaptada a móviles y tablets, con modo oscuro en menús y alertas animadas (SweetAlert2).

## 🛠️ Tecnologías Utilizadas

### Backend
* **Python 3**
* **Flask:** Framework web principal.
* **Flask-SQLAlchemy:** ORM para manejo de base de datos.
* **Flask-Login:** Gestión de sesiones y seguridad.
* **Pandas & OpenPyXL:** Generación de reportes Excel.

### Frontend
* **HTML5 / CSS3**
* **Bootstrap 5:** Framework de diseño responsivo.
* **Chart.js:** Gráficos interactivos.
* **SweetAlert2:** Alertas y notificaciones modales.
* **FontAwesome / Bootstrap Icons:** Iconografía.

### Base de Datos
* **MySQL:** Motor de base de datos relacional.

---

## ⚙️ Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en tu entorno local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/Bcortes-R/web_app_inventario.git
cd invapp
```

### 2. Crear y activar entorno virtual

**Bash**

```
# En Windows
python -m venv venv
.\venv\Scripts\activate

# En Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

**Bash**

```
pip install -r requirements.txt
```

### 4. Configurar la Base de Datos

1. Asegúrate de tener MySQL corriendo.
2. Ejecuta el script **`database/ScriptBaseDatosInventario.sql`** en tu gestor de base de datos para crear la estructura.
3. Configura tus credenciales en el archivo `config.py`:

**Python**

```
DB_USER = 'tu_usuario'
DB_PASS = 'tu_contraseña'
DB_HOST = 'localhost'
DB_NAME = 'inventario'
```

### 5. Crear Usuario Administrador

Para poder entrar por primera vez, ejecuta el script de inicialización:

**Bash**

```
python crear_admin.py
```

 *(Esto creará el usuario `admin@empresa.com` con contraseña `123456`)* .

### 6. Ejecutar la aplicación

**Bash**

```
python app.py
```

Abre tu navegador en `http://127.0.0.1:5000`

---

## 📖 Uso

### Credenciales por defecto

* **Email:** `admin@empresa.com`
* **Contraseña:** `123456`

### Flujo de Trabajo

1. **Crear Parámetros:** Ve a *Administración* > *Departamentos/Categorías* para configurar las áreas.
2. **Registrar Equipos:** Ingresa nuevos activos en el módulo  *Inventario* .
3. **Asignar:** Presta equipos a usuarios desde el módulo  *Asignaciones* .
4. **Mantenimiento:** Si un equipo falla, regístralo en  *Mantenimiento* . Su estado cambiará automáticamente.

---

## 📂 Estructura del Proyecto

```
invapp/
├── app.py                 # Punto de entrada de la aplicación
├── config.py              # Configuración de BD y claves
├── extensions.py          # Inicialización de extensiones (DB, Login)
├── crear_admin.py         # Script para crear primer usuario
├── database/		   # Modelos de Base de Datos (ORM)   
│   ├── models.py
│   └── ScriptBaseDatosInventario.sql # ESQUEMA SQL
├── routes/                # Controladores / Lógica de negocio
│   ├── auth.py            # Login/Logout
│   ├── dashboard.py       # Estadísticas
│   ├── inventario.py      # CRUD Equipos + Excel
│   ├── usuarios.py        # Gestión de Usuarios
│   ├── asignaciones.py    # Préstamos
│   ├── mantenimientos.py  # Reparaciones
│   └── parametros.py      # Deptos y Categorías
├── static/
│   └── css/
│       └── styles.css     # Estilos personalizados
├── templates/             # Vistas HTML (Jinja2)
│   ├── base.html          # Plantilla maestra
│   ├── login.html
│   ├── dashboard.html
│   └── ... (carpetas por módulo)
└── requirements.txt       # Lista de dependencias
```

## 👤 Autores

Desarrollado por  **Nicole, Camilo, Brayan ** .
Proyecto final de Bases de Datos.
