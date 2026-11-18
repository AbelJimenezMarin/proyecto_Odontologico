"""Modelos Tratamiento y SesionTratamiento (RF-05). Aquí viven las reglas RN-02 y RN-04."""
from decimal import Decimal

from django.db import models
from django.db.models import Q, Sum
from django.utils import timezone

from pacientes.models import Paciente


class Tratamiento(models.Model):
    ESTADOS = [(e, e) for e in ["En curso", "Concluido", "Cancelado"]]

    id_tratamiento = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, db_column="id_paciente", related_name="tratamientos")
    tipo = models.CharField("Tipo de tratamiento", max_length=100)
    descripcion = models.CharField("Descripción", max_length=300, blank=True, null=True)
    costo_total = models.DecimalField("Costo total (S/)", max_digits=10, decimal_places=2)
    num_sesiones = models.PositiveIntegerField("N.º de sesiones")
    estado = models.CharField(max_length=15, choices=ESTADOS, default="En curso")
    fecha_inicio = models.DateField(default=timezone.localdate)

    class Meta:
        db_table = "Tratamiento"
        ordering = ["-fecha_inicio", "-id_tratamiento"]
        constraints = [
            models.CheckConstraint(condition=Q(costo_total__gte=0), name="CK_Tratamiento_costo"),
            models.CheckConstraint(condition=Q(num_sesiones__gt=0), name="CK_Tratamiento_sesion"),
            models.CheckConstraint(condition=Q(estado__in=["En curso", "Concluido", "Cancelado"]),
                                name="CK_Tratamiento_estado"),
        ]


# ----- Avance de las sesiones -----
    @property
    def sesiones_realizadas(self):
        return self.sesiones.filter(estado="Realizada").count()

    @property
    def porcentaje_avance(self):
        return int(self.sesiones_realizadas * 100 / self.num_sesiones)

    def actualizar_estado(self):
        """RN-02: el tratamiento solo pasa a Concluido cuando se completaron TODAS sus sesiones."""
        if self.estado == "Cancelado":
            return
        nuevo = "Concluido" if self.sesiones_realizadas >= self.num_sesiones else "En curso"
        if nuevo != self.estado:
            self.estado = nuevo
            self.save(update_fields=["estado"])

    # ----- Dinero (RN-04) -----
    @property
    def total_pagado(self):
        return self.pagos.aggregate(total=Sum("monto"))["total"] or Decimal("0.00")

    @property
    def saldo_pendiente(self):
        """RN-04: saldo pendiente = costo total - pagos registrados."""
        return self.costo_total - self.total_pagado

    @property
    def clase_insignia(self):
        return {"En curso": "insignia-encurso", "Concluido": "insignia-atendida", "Cancelado": "insignia-cancelada"}[self.estado]

    def __str__(self):
        return "%s - %s" % (self.tipo, self.paciente.apellidos_nombres)


class SesionTratamiento(models.Model):
    ESTADOS = [("Pendiente", "Pendiente"), ("Realizada", "Realizada")]

    id_sesion = models.AutoField(primary_key=True)
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.PROTECT, db_column="id_tratamiento", related_name="sesiones")
    numero_sesion = models.PositiveIntegerField("N.º")
    fecha_sesion = models.DateField("Fecha")
    observaciones = models.CharField(max_length=500, blank=True, null=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default="Realizada")

    class Meta:
        db_table = "SesionTratamiento"
        ordering = ["numero_sesion"]
        constraints = [
            models.UniqueConstraint(fields=["tratamiento", "numero_sesion"], name="UQ_Sesion_numero"),
            models.CheckConstraint(condition=Q(numero_sesion__gt=0), name="CK_Sesion_numero"),
        ]

        def __str__(self):
            return "Sesión %d de %s" % (self.numero_sesion, self.tratamiento)
