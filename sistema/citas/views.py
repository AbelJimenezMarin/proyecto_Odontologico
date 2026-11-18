"""Vistas de citas: registrar y listar (CU-03), confirmar, reprogramar, cancelar y atender (CU-04)."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .formularios import FormularioCita, FormularioReprogramar
from .models import Cita, ESTADOS_VIGENTES

# Acción -> (estado nuevo, estados desde los que se permite).
ACCIONES = {
    "confirmar": ("Confirmada", ["Programada", "Reprogramada"]),
    "cancelar": ("Cancelada", ESTADOS_VIGENTES),
    "atender": ("Atendida", ESTADOS_VIGENTES),
}

@login_required
def listar_citas(peticion):
    """Formulario para registrar una cita y listado de citas (desde hoy, o todo el historial)."""
    historial = peticion.GET.get("ver") == "historial"
    formulario = FormularioCita(peticion.POST or None, initial={"fecha_cita": timezone.localdate()})
    if peticion.method == "POST" and formulario.is_valid():
        cita = formulario.save(commit=False)
        cita.usuario = peticion.user                      # queda registrado quién creó la cita
        try:
            cita.save()
        except IntegrityError:                            # red de seguridad: lo detecta el índice de la base de datos
            formulario.add_error(None, "Horario ocupado: ya existe una cita para esa fecha y hora.")
        else:
            messages.success(peticion, "Cita registrada para %s." % cita.paciente.apellidos_nombres)
            return redirect("listar_citas")
    citas = Cita.objects.select_related("paciente")
    citas = citas.order_by("-fecha_cita", "-hora_cita") if historial else \
        citas.filter(fecha_cita__gte=timezone.localdate()).order_by("fecha_cita", "hora_cita")
    return render(peticion, "citas/citas.html", {
        "formulario": formulario, "citas": citas, "historial": historial, "menu": "citas"})

@login_required
@require_POST
def cambiar_estado_cita(peticion, id_cita, accion):
    cita = get_object_or_404(Cita, pk=id_cita)
    destino = peticion.POST.get("siguiente") or "listar_citas"
    if accion not in ACCIONES:
        messages.error(peticion, "Acción no válida.")
        return redirect("listar_citas")
    estado_nuevo, estados_permitidos = ACCIONES[accion]
    if cita.estado not in estados_permitidos:
        messages.error(peticion, "No se puede %s una cita %s." % (accion, cita.estado.lower()))
    else:
        cita.estado = estado_nuevo
        cita.save(update_fields=["estado"])
        messages.success(peticion, "Cita %s." % estado_nuevo.lower())
    return redirect(destino)


@login_required
def reprogramar_cita(peticion, id_cita):
    cita = get_object_or_404(Cita, pk=id_cita)
    if not cita.es_vigente:
        messages.error(peticion, "Solo se pueden reprogramar citas vigentes.")
        return redirect("listar_citas")
    formulario = FormularioReprogramar(peticion.POST or None, instance=cita)
    if peticion.method == "POST" and formulario.is_valid():
        cita = formulario.save(commit=False)
        cita.estado = "Reprogramada"
        cita.recordatorio_enviado = False                 # se volverá a avisar al paciente
        try:
            cita.save()
        except IntegrityError:
            formulario.add_error(None, "Horario ocupado: ya existe una cita para esa fecha y hora.")
        else:
            messages.success(peticion, "Cita reprogramada.")
            return redirect("listar_citas")
    return render(peticion, "citas/reprogramar_cita.html", {"formulario": formulario, "cita": cita, "menu": "citas"})
