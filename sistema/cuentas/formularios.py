"""Formulario de inicio de sesión (CU-01)."""
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

class FormularioInicioSesion(forms.Form):
    usuario = forms.CharField(
        widget=forms.TelInput(attrs={"class": "entrada", "id": "campo-usuario", "autocomplete": "username",
                                    "placeholder": "Ingrese su correo"})
    )

    clave = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "entrada", "id": "campo-clave", "autocomplete": "current-password", "placeholder": "Ingrese su contraseña"})
    )

    def __init__(self, *args, peticion=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.peticion = peticion
        self.usuario_autenticado = None

    def clean(self):
        datos = super().clean()
        correo, clave = datos.get("usuario"), datos.get("clave")
        if correo and clave:
            # authenticate() compara la clave con el hash guardado y rechaza usuarios inactivos.

            self.usuario_autenticado = authenticate(self.peticion, username=correo.strip(), password=clave)
            if self.usuario_autenticado is None:
                raise forms.ValidationError("Usuario o contraseña incorrectos.")
            return datos

class FormularioRecuperarClave(PasswordResetForm):
    """Pide el correo de la cuenta y envía el enlace para crear una contraseña nueva."""
    email = forms.EmailField(
        label="Correo", max_length=100,
        widget=forms.EmailInput(attrs={"class": "entrada", "autocomplete": "email", "placeholder": "Ingrese su correo"}))

    def get_users(self, email):
        """Solo cuentas ACTIVAS con ese correo (nuestro modelo usa el campo "activo", no "is_active")."""
        usuarios = get_user_model()._default_manager.filter(correo__iexact=email, activo=True)
        return (u for u in usuarios if u.has_usable_password())


class FormularioNuevaClave(SetPasswordForm):
    """Pide la contraseña nueva dos veces (aplica las reglas de AUTH_PASSWORD_VALIDATORS)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs["class"] = "entrada"