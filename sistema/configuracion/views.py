"""Panel Principal: resume la jornada y reúne datos de varias aplicaciones (por eso vive en el proyecto)."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from citas.models import Cita
from pacientes.models import Paciente
from tratamientos.models import Tratamiento

@login_required                 # Sin Sesión no se entra (RN-05)
def panel(peticion):
    hoy = timezone.localdate()
    citas_hoy = Cita.objects.filter(fecha_cita=hoy).select_related("paciente").order_by("hora_cita")
    tratamientos = Tratamiento.objects.exclude(estado="Cancelado")
    saldo_total = sum(t.saldo_pendiente for t in tratamientos)        # RN-04 aplicada a cada tratamiento
    return render(peticion, "panel.html", {
        "hoy": hoy,
        "citas_hoy": citas_hoy,
        "total_citas_hoy": citas_hoy.count(),
        "total_pacientes": Paciente.objects.filter(activo=True).count(),
        "total_tratamientos": Tratamiento.objects.filter(estado="En curso").count(),
        "saldo_total": saldo_total,
        "menu": "panel",
    })
