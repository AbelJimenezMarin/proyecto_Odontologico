"""Crea (o actualiza la clave de) la usuaria del sistema.

Uso: python manage.py crear_usuaria --correo dra.cynthia@ejemplo.com --nombre "Dra. Cynthia Morey"
La contraseña se pide por teclado (no se ve al escribirla) y se guarda cifrada."""

from getpass import getpass

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from cuentas.models import Usuario

class Command(BaseCommand):
    help = "Crea la cuenta de la usuaria del sistema (consultorio unipersonal, RN-05)."

    def add_arguments(self, parser):
        parser.add_argument("--correo", required=True)
        parser.add_argument("--nombre", required=True)
        parser.add_argument("--clave", help="Solo para pruebas automáticas; si se omite, se pide por teclado.")

    def handle(self, *args, **opciones):
        clave = opciones["clave"] or getpass("Contraseña: ")
        try:
            validate_password(clave)
        except ValidationError as error:
            raise CommandError("; ".join(error.messages))
        usuario, creado = Usuario.objects.get_or_create(
            correo=opciones["correo"], defaults={"nombre_completo": opciones["nombre"]})
        usuario.set_password(clave)
        usuario.nombre_completo = opciones["nombre"]
        usuario.save()
        self.stdout.write(self.style.SUCCESS("Usuaria %s." % ("creada" if creado else "actualizada")))

