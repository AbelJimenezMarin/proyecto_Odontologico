"""Vista de pagos: resumen del tratamiento, registro de pagos e historial (CU-06)."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from tratamientos.models import Tratamiento

from .formularios import FormularioPago

@login_required
def registrar_pago(peticion):
    tratamientos = Tratamiento.objects.exclude(estado="Cancelado").select_related("paciente")
    # El tratamiento se elige con ?tratamiento=ID; si no se indica, se toma el primero que aún tenga saldo.
    id_elegido = peticion.POST.get("tratamiento") or peticion.GET.get("tratamiento")
    elegido = tratamientos.filter(pk=id_elegido).first() if id_elegido else None
    if elegido is None:
        elegido = next((t for t in tratamientos if t.saldo_pendiente > 0), tratamientos.first())
    formulario = FormularioPago(peticion.POST or None, tratamiento=elegido, initial={"fecha_pago": timezone.localdate()})
    if elegido and peticion.method == "POST" and formulario.is_valid():
        pago = formulario.save(commit=False)
        pago.tratamiento = elegido
        pago.save()
        messages.success(peticion, "Pago registrado. Saldo pendiente: S/ %s." % elegido.saldo_pendiente)
        return redirect("%s?tratamiento=%s" % (peticion.path, elegido.pk))
    return render(peticion, "pagos/pagos.html", {
        "tratamientos": tratamientos, "tratamiento": elegido, "formulario": formulario,
        "pagos": elegido.pagos.all() if elegido else [], "menu": "pagos"})


