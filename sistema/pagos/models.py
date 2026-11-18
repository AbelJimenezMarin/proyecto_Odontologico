"""Modelo Pago (tabla Pago). El saldo pendiente (RN-04) se calcula en Tratamiento.saldo_pendiente."""

from django.db import models
from django.db.models import Q
from django.utils import timezone

from tratamientos.models import Tratamiento

class Pago(models.Model):
    METODOS = [(m, m) for m in ["Efectivo", "Yape", "Plin", "Transferencia", "Tarjeta"]] 

    id_pago = models.AutoField(primary_key=True)
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.PROTECT, db_column="id_tratamiento", related_name="pagos")
    monto = models.DecimalField("Monto (S/)", max_digits=10, decimal_places=2)
    fecha_pago = models.DateField("Fecha de pago", default=timezone.localdate)
    metodo_pago = models.CharField("Método de pago", max_length=20, choices=METODOS, default="Efectivo")

    class Meta:
        db_table = "Pago"
        ordering = ["-fecha_pago", "-id_pago"]
        constraints = [
            models.CheckConstraint(condition=Q(monto__gt=0), name="CK_Pago_monto"),
            models.CheckConstraint(condition=Q(metodo_pago__in=["Efectivo", "Yape", "Plin", "Transferencia", "Tarjeta"]), name="CK_Pago_metodo"),
        ]

    def __str__(self):
        return "S/ %s - %s" % (self.monto, self.tratamiento)