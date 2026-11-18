from django.urls import path

from . import views

urlpatterns = [
    path("", views.registrar_pago, name="registrar_pago"),
]
