"""Vistas de atención de pacientes (CU-05): ficha, historial, tratamientos y sesiones."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from citas.models import Cita
from pacientes.models import Paciente
from .formularios import FormularioSesion, FormularioTratamiento
from .models import SesionTratamiento, Tratamiento


def _mostrar_errores(peticion, formulario):
    """Convierte los errores de un formulario en mensajes rojos (los formularios de esta pantalla son varios)."""
    for campo, errores in formulario.errors.items():
        for error in errores:
            messages.error(peticion, error)

@login_required
def elegir_paciente(peticion):
    """Pantalla inicial de Atención: lista de pacientes activos para abrir su ficha."""
    pacientes = Paciente.objects.filter(activo=True)
    return render(peticion, "tratamientos/elegir_paciente.html", {"pacientes": pacientes, "menu": "atencion"})


@login_required
def ficha_paciente(peticion, id_paciente):
    paciente = get_object_or_404(Paciente, pk=id_paciente)
    cita_actual = None
    if peticion.GET.get("cita"):                                   # llegó desde "Atender" de la agenda
        cita_actual = Cita.objects.filter(pk=peticion.GET["cita"], paciente=paciente).first()
    return render(peticion, "tratamientos/ficha_paciente.html", {
        "paciente": paciente,
        "cita_actual": cita_actual,
        "citas": paciente.citas.order_by("-fecha_cita", "-hora_cita")[:10],     # historial reciente
        "tratamientos": paciente.tratamientos.prefetch_related("sesiones"),
        "formulario_tratamiento": FormularioTratamiento(),
        "hoy": timezone.localdate(),
        "menu": "atencion",
    })

@login_required
@require_POST
def registrar_tratamiento(peticion, id_paciente):
    paciente = get_object_or_404(Paciente, pk=id_paciente)
    formulario = FormularioTratamiento(peticion.POST)
    if formulario.is_valid():
        tratamiento = formulario.save(commit=False)
        tratamiento.paciente = paciente
        tratamiento.save()
        messages.success(peticion, "Tratamiento registrado: %s." % tratamiento.tipo)
    else:
        _mostrar_errores(peticion, formulario)
    return redirect("ficha_paciente", id_paciente=paciente.pk)

@login_required
@require_POST
def registrar_sesion(peticion, id_tratamiento):
    tratamiento = get_object_or_404(Tratamiento, pk=id_tratamiento)
    destino = redirect("ficha_paciente", id_paciente=tratamiento.paciente_id)
    if tratamiento.estado != "En curso":
        messages.error(peticion, "Solo se registran sesiones en tratamientos en curso.")
        return destino
    formulario = FormularioSesion(peticion.POST)
    if not formulario.is_valid():
        _mostrar_errores(peticion, formulario)
        return destino
    ultimo = tratamiento.sesiones.aggregate(m=Max("numero_sesion"))["m"] or 0
    if ultimo >= tratamiento.num_sesiones:
        messages.error(peticion, "El tratamiento ya tiene todas sus sesiones registradas.")
        return destino
    sesion = formulario.save(commit=False)
    sesion.tratamiento = tratamiento
    sesion.numero_sesion = ultimo + 1                  # el número lo calcula el sistema
    sesion.estado = "Realizada"
    sesion.save()
    tratamiento.actualizar_estado()                    # RN-02
    if tratamiento.estado == "Concluido":
        messages.success(peticion, "Sesión %d registrada. El tratamiento quedó CONCLUIDO." % sesion.numero_sesion)
    else:
        messages.success(peticion, "Sesión %d registrada." % sesion.numero_sesion)
    return destino
