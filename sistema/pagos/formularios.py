"""Formulario de pagos (CU-06). Valida que el monto no supere el saldo pendiente (RN-04)."""

from django import forms

from .models import Pago

class FormularioPago(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ["monto", "metodo_pago", "fecha_pago"]
        widgets = {"monto": forms.NumberInput(attrs={"class": "entrada", "id": "campo-monto", "step": "0.01", "min": "0",
                    "inputmode": "decimal"}), "metodo_pago": forms.Select(attrs={"class": "selector", "id": "selector-metodo-pago"}),
                    "fecha_pago": forms.DateInput(format="%Y-%m-%d", attrs={"class": "entrada", "type": "date", "id": "campo-fecha-pago"}),}

    def __init__(self, *args, tratamiento=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tratamiento = tratamiento

    def clean_monto(self):
        monto = self.cleaned_data["monto"]
        if monto <= 0:
            raise forms.ValidationError("El monto debe ser mayor que 0.")
        if self.tratamiento is not None and monto > self.tratamiento.saldo_pendiente:
            raise forms.ValidationError("El monto no puede superar el saldo pendiente (S/ %s)." % self.tratamiento.saldo_pendiente)
        return monto
