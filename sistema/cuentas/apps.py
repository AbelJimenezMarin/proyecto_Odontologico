from django.apps import AppConfig

class CuentasConfig(AppConfig):
    name = "cuentas"

    def ready(self):
        # Django intenta guardar "last_login" al ingresar; como nuestra tabla no tiene esa columna,
        # se desconecta esa señal para que no falle.
        from django.contrib.auth import user_logged_in
        from django.contrib.auth.models import update_last_login
        user_logged_in.disconnect(update_last_login)

