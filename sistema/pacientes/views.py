"""Vistas de pacientes: listar y registrar, editar, desactivar y reactivar (RN-03)."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .formularios import FormularioPaciente
from .models import Paciente

@login_required
def listar_pacientes(peticion):
    """Muestra el formulario de registro y el listado (solo activos, o inactivos con ?ver=inactivos)."""
    ver_inactivos = peticion.GET.get("ver") == "inactivos"
    formulario = FormularioPaciente(peticion.POST or None)
    if peticion.method == "POST" and formulario.is_valid():
        paciente = formulario.save()
        messages.success(peticion, "Paciente registrado: %s." % paciente.apellidos_nombres)
        return redirect("listar_pacientes")
    pacientes = Paciente.objects.filter(activo=not ver_inactivos)
    return render(peticion, "pacientes/pacientes.html", {
        "formulario": formulario, "pacientes": pacientes, "ver_inactivos": ver_inactivos, "menu": "pacientes"})

@login_required
def editar_paciente(peticion, id_paciente):
    paciente = get_object_or_404(Paciente, pk=id_paciente)
    formulario = FormularioPaciente(peticion.POST or None, instance=paciente)
    if peticion.method == "POST" and formulario.is_valid():
        formulario.save()
        messages.success(peticion, "Datos actualizados.")
        return redirect("listar_pacientes")
    return render(peticion, "pacientes/editar_paciente.html", {
        "formulario": formulario, "paciente": paciente, "menu": "pacientes"})

@login_required
@require_POST
def cambiar_estado_paciente(peticion, id_paciente):
    """RN-03: en lugar de eliminar, se desactiva (o se reactiva) al paciente."""
    paciente = get_object_or_404(Paciente, pk=id_paciente)
    paciente.activo = not paciente.activo
    paciente.save(update_fields=["activo"])
    messages.success(peticion, "Paciente %s." % ("reactivado" if paciente.activo else "desactivado"))
    return redirect("listar_pacientes")