from django.contrib.auth import views as vistas_auth
from django.urls import path, reverse_lazy

from . import views
from .formularios import FormularioNuevaClave, FormularioRecuperarClave

urlpatterns = [
    path("ingresar/", views.iniciar_sesion, name="iniciar_sesion"),
    path("salir/", views.cerrar_sesion, name="cerrar_sesion"),

    # ---- Recuperar contraseña (vistas que ya trae Django; aquí solo se configuran) ----
    path("recuperar/", vistas_auth.PasswordResetView.as_view(
        template_name="cuentas/recuperar_clave.html",
        form_class=FormularioRecuperarClave,
        email_template_name="cuentas/correo_recuperar_clave.txt",
        subject_template_name="cuentas/correo_recuperar_asunto.txt",
        success_url=reverse_lazy("recuperar_clave_enviado")), name="recuperar_clave"),
    path("recuperar/enviado/", vistas_auth.PasswordResetDoneView.as_view(
        template_name="cuentas/recuperar_clave_enviado.html"), name="recuperar_clave_enviado"),
    path("recuperar/<uidb64>/<token>/", vistas_auth.PasswordResetConfirmView.as_view(
        template_name="cuentas/restablecer_clave.html",
        form_class=FormularioNuevaClave,
        success_url=reverse_lazy("restablecer_clave_completo")), name="restablecer_clave"),
    path("recuperar/completo/", vistas_auth.PasswordResetCompleteView.as_view(
        template_name="cuentas/restablecer_clave_completo.html"), name="restablecer_clave_completo"),
]