"""Formularios de citas (CU-03 registrar y CU-04 reprogramar)."""
from django import forms
from django.utils import timezone

from pacientes.models import Paciente

from .models import Cita, ESTADOS_VIGENTES


def horario_ocupado(fecha, hora, excluir_pk=None):
    """RN-01: True si ya existe otra cita VIGENTE en esa fecha y hora."""
    ocupadas = Cita.objects.filter(fecha_cita=fecha, hora_cita=hora, estado__in=ESTADOS_VIGENTES)
    if excluir_pk:
        ocupadas = ocupadas.exclude(pk=excluir_pk)
    return ocupadas.exists()

class FormularioCita(forms.ModelForm):
    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.filter(activo=True), label="Paciente", empty_label="Seleccione un paciente",
        widget=forms.Select(attrs={"class": "selector", "id": "selector-paciente"}))

    class Meta:
        model = Cita
        fields = ["paciente", "fecha_cita", "hora_cita", "motivo"]
        widgets = {
            "fecha_cita": forms.DateInput(format="%Y-%m-%d", attrs={"class": "entrada", "type": "date", "id": "campo-fecha-cita"}),
            "hora_cita": forms.TimeInput(format="%H:%M", attrs={"class": "entrada", "type": "time", "id": "campo-hora-cita"}),
            "motivo": forms.TextInput(attrs={"class": "entrada", "id": "campo-motivo"}),
        }

    def clean(self):
        datos = super().clean()
        fecha, hora = datos.get("fecha_cita"), datos.get("hora_cita")
        if fecha and hora and horario_ocupado(fecha, hora, self.instance.pk):
            raise forms.ValidationError("Horario ocupado: ya existe una cita para esa fecha y hora. Elija otra hora.")
        return datos

class FormularioReprogramar(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ["fecha_cita", "hora_cita"]
        widgets = FormularioCita.Meta.widgets.copy()

    def clean(self):
        datos = super().clean()
        fecha, hora = datos.get("fecha_cita"), datos.get("hora_cita")
        if fecha and hora and horario_ocupado(fecha, hora, self.instance.pk):
            raise forms.ValidationError("Horario ocupado: ya existe una cita para esa fecha y hora. Elija otra hora.")
        return datos
