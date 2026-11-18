"""
Ajustes del proyecto Sistema Web NADINNE (Djando 5.2)
Los datos delicados (claves, usuario de la base de datos) se leen del archivo .env,
que NO se sube a GitHub. Ver .env.ejemplo.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# BASE_DIR = carpeta "sistema" (donde esta manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent
# Lee el archivo .env que está en la carpeta raíz del proyecto (proyecto_Odontologico).
load_dotenv(BASE_DIR.parent / ".env")

# ============ SEGURIDAD ============
SECRET_KEY = os.getenv("DJANGO_CLAVE_SECRETA", "clave-solo-para-desarrollo-no-usar-en-produccion")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("DJANGO_HOSTS_PERMITIDOS", "localhost,127.0.0.1").split(",")

# ========== APLICACIONES =============
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Aplicaciones propias (una por módulo)
    "cuentas",
    "pacientes",
    "citas",
    "tratamientos",
    "pagos",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",             # protección CSRF en los formularios
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "configuracion.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "plantillas"],           # carpeta con base.html y las pantallas
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "configuracion.wsgi.application"

# ============ BASE DE DATOS =============
# BD_MOTOR=sqlserver -> SQL Server (uso normal del proyecto).
# BD_MOTOR=sqlite    -> SOLO para ejecutar las pruebas automáticas sin SQL Server.
if os.getenv("BD_MOTOR", "sqlserver") == "sqlite":
    DATABASES = {
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "pruebas.sqlite3"},
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "mssql",        # controlador mssql-django
            "NAME": os.getenv("BD_NOMBRE", "BD_NADINNE"),
            "USER": os.getenv("BD_USUARIO", ""),
            "PASSWORD": os.getenv("BD_CLAVE", ""),
            "HOST": os.getenv("BD_SERVIDOR", "localhost"),
            "PORT": "",
            "OPTIONS": {
                "driver": os.getenv("BD_DRIVER", "ODBC Driver 18 for SQL Server"),
                # El Driver 18 exige cifrado; en una instalación local se confia en el certificado.
                "extra_params": "TrustServerCertificate=yes",
            },
        }
    }

# ============ USUARIOS Y SESIONES ============
AUTH_USER_MODEL = "cuentas.Usuario"             # modelo propio (tabla Usuario)
LOGIN_URL = "iniciar_sesion"                    # a dónde se envia a quien lo ha ingresado
LOGIN_REDIRECT_URL = "panel"                    # a dónde se va después de ingresar.
LOGOUT_REDIRECT_URL = "iniciar_sesion"
SESSION_COOKIE_AGE = 30 * 60                    # La sesión caduca a los 30 minutos...
SESSION_SAVE_EVERY_REQUEST = True               # ...de inactividad (se renueva en cada petición)
SESSION_COOKIE_HTTPONLY = True
PASSWORD_RESET_TIMEOUT = 60 * 60

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
]

# =========== IDIOMA Y HORA ===========
LANGUAGE_CODE = "es-pe"
TIME_ZONE = "America/Lima"
USE_I18N = True
USE_TZ = True

# =========== ARCHIVOS ESTÁTICOS (css, js, imágenes) ==============
STATIC_URL = "/estaticos/"
STATICFILES_DIRS = [BASE_DIR / "estaticos"]

# ============ CORREO ============
if os.getenv("CORREO_SERVIDOR"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("CORREO_SERVIDOR")
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv("CORREO_USUARIO", "")
    EMAIL_HOST_PASSWORD = os.getenv("CORREO_CLAVE", "")
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"      # Los correos salen en la consola.
    DEFAULT_FROM_EMAIL = "Consultorio NADINNE <no-responder@nadinne.local>"

    DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
    

