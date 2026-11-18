from django.urls import path

from . import views

urlpatterns = [
    path("", views.listar_citas, name="listar_citas"),
    # IMPORTANTE: la ruta de reprogramar va ANTES de la ruta general <accion>; si no, Django la confundiría con una acción.
    path("<int:id_cita>/reprogramar/", views.reprogramar_cita, name="reprogramar_cita"),
    path("<int:id_cita>/<str:accion>/", views.cambiar_estado_cita, name="cambiar_estado_cita"),
]
