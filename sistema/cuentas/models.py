"""Modelo Usuario: la cuenta de la Dra. Cynthia (tabla Usuario de la base de datos)."""

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

class AdministradorUsuarios(BaseUserManager):
    """Sabe crear usuarios con la contraseña cifrada (hash), nunca en texto plano."""
    def create_user(self, correo, nombre_completo, password=None, **extra):
        if not correo:
            raise ValueError("El correo es obligatorio.")
        usuario = self.model(correo=self.normalize_email(correo),
                            nombre_completo=nombre_completo, **extra)
        usuario.set_password(password)      # cifra la contraseña (PBKDF2) antes de guadarla
        usuario.save(using=self._db)
        return usuario

class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True)
    nombre_completo = models.CharField("Nombre completo", max_length=100)
    correo = models.EmailField("Correo", max_length=100, unique=True)
    # La contraseña cifrada se guarda en la columna clave_hash
    password = models.CharField("Clave (hash)", max_length=255, db_column="clave_hash")
    rol = models.CharField(max_length=20, default="Administrador")
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    last_login = None               # la tabla Usuario no tiene esta columna: se quita

    USERNAME_FIELD = "correo"           # se ingresa el correo
    EMAIL_FIELD = "correo"              # Django envía aqui el enlace de recuperar contraseña
    REQUIRED_FIELDS = ["nombre_completo"]
    objects = AdministradorUsuarios()

    class Meta:
        db_table = "Usuario"

    @property
    def is_active(self):
        """Django consulta esta peopiedad: un usuario con activo = 0 no puede ingresar."""
        return self.activo

    @property
    def iniciales(self):
        """Dos letras para el círculo del menú lateral (por ejemplo, CM)."""
        partes = [p for p in self.nombre_completo.replace("Dra.", "").replace("Dr.", "").split() if p]
        return "".join(p[0] for p in partes[:2]).upper() or "U"

    def __str__(self):
        return self.nombre_completo
    