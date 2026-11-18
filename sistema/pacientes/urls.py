from django.urls import path

from . import views

urlpatterns = [
    path("", views.listar_pacientes, name="listar_pacientes"),
    path("<int:id_paciente>/editar/", views.editar_paciente, name="editar_paciente"),
    path("<int:id_paciente>/estado/", views.cambiar_estado_paciente, name="cambiar_estado_paciente"),
]
