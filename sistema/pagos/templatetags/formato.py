"""Filtro de plantilla para mostrar dinero igual que el prototipo: S/. 1,200.00"""

from decimal import Decimal

from django import template

register = template.Library()

@register.filter
def soles(valor):
    """Convierte 1200 en 'S/ 1,200.00' (coma de miles y punto decimal, como se escribe en el Perú)."""
    return "S/ {:,.2f}".format(Decimal(valor or 0))

