"""Modelo Paciente (tabla Paciente) RN-03: los pacientes no se eliminan, sólo se desactivan."""

from datetime import date

from django.core.validators import RegexValidator
from django.db import models

class Paciente(models.Model):
    SEXOS = [("F", "Femenino"), ("M", "Masculino")]
    id_paciente = models.AutoField(primary_key=True)
    dni = models.CharField("DNI", max_length=8, unique=True, error_messages={"unique": "Ya existe un paciente con este DNI."}, validators=[RegexValidator(r"^[0-9]{8}$", "El DNI debe tener 8 dígitos.")])
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    fecha_nacimiento = models.DateField("Fecha de nacimiento")
    sexo = models.CharField(max_length=1, choices=SEXOS)
    telefono = models.CharField("Teléfono", max_length=15)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    direccion = models.CharField("Dirección", max_length=150, blank=True, null=True)
    antecedentes = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)          # RN-03
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Paciente"
        ordering = ["apellidos", "nombres"]
        constraints = [models.CheckConstraint(condition=models.Q(sexo__in=["M", "F"]), name="CK_Paciente_sexo"),]

    @property
    def apellidos_nombres(self):
        return "%s, %s" % (self.apellidos, self.nombres)

    @property
    def nombre_completo(self):
        return "%s %s" % (self.nombres, self.apellidos)

    @property
    def edad(self):
        hoy = date.today()
        antes_de_cumple = (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        return hoy.year - self.fecha_nacimiento.year - antes_de_cumple

    def __str__(self):
        return self.apellidos_nombres
    


        