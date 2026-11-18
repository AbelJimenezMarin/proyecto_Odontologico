"""Modelo Cita (tabla Cita). RN-01: no puede haber dos citas vigentes en la misma fecha y hora."""
from django.db import models
from django.db.models import Q

from pacientes.models import Paciente

# Estados que ocupan el horario. Una cita Cancelada o Atendida libera la hora.
ESTADOS_VIGENTES = ["Programada", "Confirmada", "Reprogramada"]
# Todos los estados posibles de una cita.
TODOS_LOS_ESTADOS = ESTADOS_VIGENTES + ["Cancelada", "Atendida"]


class Cita(models.Model):
    ESTADOS = [(e, e) for e in TODOS_LOS_ESTADOS]
    id_cita = models.AutoField(primary_key=True)
    # PROTECT: no se puede borrar un paciente que tenga citas (RN-03).
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, db_column="id_paciente", related_name="citas")
    usuario = models.ForeignKey("cuentas.Usuario", on_delete=models.PROTECT, db_column="id_usuario")
    fecha_cita = models.DateField("Fecha")
    hora_cita = models.TimeField("Hora")
    estado = models.CharField(max_length=15, choices=ESTADOS, default="Programada")
    motivo = models.CharField("Motivo de la consulta", max_length=200, blank=True, null=True)
    recordatorio_enviado = models.BooleanField(default=False)     # RF-07
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Cita"
        ordering = ["fecha_cita", "hora_cita"]
        constraints = [
            # RN-01 en la base de datos: índice único filtrado (solo cuenta las citas vigentes).
            models.UniqueConstraint(fields=["fecha_cita", "hora_cita"],
                                    condition=Q(estado__in=ESTADOS_VIGENTES),
                                    name="UX_Cita_fecha_hora_vigente"),
            models.CheckConstraint(condition=Q(estado__in=TODOS_LOS_ESTADOS), name="CK_Cita_estado"),
        ]









        

@property
def es_vigente(self):
        return self.estado in ESTADOS_VIGENTES

@property
def clase_insignia(self):
        """Clase CSS de la etiqueta de color según el estado."""
        return {"Programada": "insignia-programada", "Reprogramada": "insignia-programada",
                "Confirmada": "insignia-confirmada", "Atendida": "insignia-atendida",

"Cancelada": "insignia-cancelada"}[self.estado]

def __str__(self):
        return "%s %s - %s" % (self.fecha_cita, self.hora_cita.strftime("%H:%M"), self.paciente)
