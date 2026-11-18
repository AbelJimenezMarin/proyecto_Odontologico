"""Vistas de las cuentas: iniciar sesion y cerrar sesion (CU-01)."""
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .formularios import FormularioInicioSesion

def iniciar_sesion(peticion):
    if peticion.user.is_authenticated:
        return redirect("panel")
    formulario = FormularioInicioSesion(peticion.POST or None, peticion=peticion)
    if peticion.method == "POST" and formulario.is_valid():
        login(peticion, formulario.usuario_autenticado)       # abre la sesión
        return redirect(peticion.GET.get("siguiente") or "panel")
    return render(peticion, "cuentas/iniciar_sesion.html", {"formulario": formulario})

@require_POST               # cerrar sesión solo se acepta por POST
def cerrar_sesion(peticion):
    logout(peticion)
    return redirect("iniciar_sesion")


