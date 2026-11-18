"""Rutas principales: cada aplicación aporta sus propias rutas"""
from django.urls import include, path
from django.shortcuts import redirect

from .views import panel

urlpatterns = [
    path("", lambda peticion: redirect("panel")),                     # la raiz lleva al panel principal
    path("panel/", panel, name="panel"),
    path("", include("cuentas.urls")),                                # /ingresar/, /salir/
    path("pacientes/", include("pacientes.urls")),
    path("citas/", include("citas.urls")),
    path("atencion/", include("tratamientos.urls")),
    path("pagos/", include("pagos.urls")),
]


