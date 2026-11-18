"""Formulario para registrar y editar pacientes (CU-02)."""

from django import forms

from .models import Paciente

class FormularioPaciente(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ["dni", "nombres", "apellidos", "fecha_nacimiento", "sexo", "telefono", "correo", "direccion", "antecedentes"]
        # Cada campo conserva los mismo id y clases CSS del prototipo, para reutilizar CSS y JS.
        widgets = {"dni": forms.TextInput(attrs={"class": "entrada", "id": "campo-dni", "maxlength": "8", "inputmode": "numeric", "placeholder": "8 dígitos"}),
                    "nombres": forms.TextInput(attrs={"class": "entrada", "id": "campo-nombres"}),
                    "apellidos": forms.TextInput(attrs={"class": "entrada", "id": "campo-apellidos"}),
                    "fecha_nacimiento": forms.DateInput(format="%Y-%m-%d", attrs={"class": "entrada", "type": "date", "id": "campo-fecha-nacimiento"}),
                    "sexo": forms.Select(attrs={"class": "selector", "id": "campo-sexo"}),
                    "telefono": forms.TextInput(attrs={"class": "entrada", "type": "tel", "id": "campo-telefono", "inputmode": "tel"}),
                    "correo": forms.EmailInput(attrs={"class": "entrada", "id": "campo-correo"}),
                    "direccion": forms.TextInput(attrs={"class": "entrada", "id": "campo-direccion"}),
                    "antecedentes": forms.Textarea(attrs={"class": "area-texto", "id": "campo-antecedentes"}),
                    }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["sexo"].choices = Paciente.SEXOS        # sin la opción en blanco: Femenino / Masculino

        def clean_correo(self):
            return self.cleaned_data.get("correo") or None       # un correo vacío se guarda como NULL