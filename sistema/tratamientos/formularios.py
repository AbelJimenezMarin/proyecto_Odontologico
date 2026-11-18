"""Formularios del módulo de atención: nuevo tratamiento y registro de sesión."""
from django import forms

from .models import SesionTratamiento, Tratamiento


class FormularioTratamiento(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ["tipo", "descripcion", "costo_total", "num_sesiones"]
        widgets = {
            "tipo": forms.TextInput(attrs={"class": "entrada", "id": "campo-tipo-tratamiento"}),
            "descripcion": forms.TextInput(attrs={"class": "entrada", "id": "campo-descripcion-tratamiento"}),
            "costo_total": forms.NumberInput(attrs={"class": "entrada", "id": "campo-costo-total", "step": "0.01", "min": "0", "inputmode": "decimal"}),
            "num_sesiones": forms.NumberInput(attrs={"class": "entrada", "id": "campo-num-sesiones", "min": "1"}),
        }

class FormularioSesion(forms.ModelForm):
    observaciones = forms.CharField(max_length=500, label="Observaciones clínicas", error_messages={"required": "Escriba las observaciones clínicas de la sesión."})

    class Meta:
        model = SesionTratamiento
        fields = ["fecha_sesion", "observaciones"]
