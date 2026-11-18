from django.urls import path

from . import views

urlpatterns = [
    path("", views.elegir_paciente, name="elegir_paciente"),
    path("<int:id_paciente>/", views.ficha_paciente, name="ficha_paciente"),
    path("<int:id_paciente>/tratamiento/nuevo/", views.registrar_tratamiento, name="registrar_tratamiento"),
    path("tratamiento/<int:id_tratamiento>/sesion/", views.registrar_sesion, name="registrar_sesion"),
]
