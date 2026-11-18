"""Carga datos de prueba FICTICIOS (pacientes, citas, tratamientos y pagos) para probar el sistema.

Uso: python manage.py cargar_datos_prueba
Anes hay que crear la usuaria: python manage.py crear_usuaria --correo... --nombre...
Solo se ejecuta si todavía no hay pacientes (RNF-05: durante el desarrollo solo se usan datos de prueba)."""

from datetime import date, time, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from citas.models import Cita
from cuentas.models import Usuario
from pacientes.models import Paciente
from pagos.models import Pago
from tratamientos.models import SesionTratamiento, Tratamiento

class Command(BaseCommand):
    help = "Carga datos de prueba ficticios."

    def handle(self, *args, **opciones):
        usuaria = Usuario.objects.first()
        if usuaria is None:
            raise CommandError("Primero cree la usuaria con: python manage.py crear_usuaria")
        if Paciente.objects.exists():
            self.stdout.write("Ya hay pacientes registrados: no se cargó nada.")
            return
        hoy = timezone.localdate()

        def paciente(dni, nombres, apellidos, nacimiento, sexo, telefono, correo, antecedentes=""):
            return Paciente.objects.create(dni=dni, nombres=nombres, apellidos=apellidos, fecha_nacimiento=nacimiento, sexo=sexo,
                                        telefono=telefono, correo=correo, antecedentes=antecedentes)

        maria = paciente("72145896", "María", "Quispe Ramírez", date(1990, 5, 14), "F", "987 654 321", "maria.quispe@correo.test")
        luis = paciente("45871236", "Luis", "Pérez Vásquez", date(1985, 11, 2), "M", "965 120 874", "luis.perez@correo.test")
        rosa = paciente("60254781", "Rosa", "Díaz Tuanama", date(1978, 3, 21), "F", "912 345 678", "rosa.diaz@correo.test")
        carlos = paciente("41236985", "Carlos", "Ríos Flores", date(1969, 8, 30), "M", "934 567 812", None)
        ana = paciente("46325178", "Ana", "Torres Pinedo", date(1992, 1, 9), "F", "945 221 330", "ana.torres@correo.test", "Alergia a la penicilina. Sin enfermedades crónicas.")
        jorge = paciente("73659412", "Jorge", "Salas Mori", date(2000, 7, 17), "M", "956 778 120", "jorge.salas@correo.test")

        def cita(pac, dias, hora, estado, motivo):
            Cita.objects.create(paciente=pac, usuario=usuaria, fecha_cita=hoy + timedelta(days=dias), hora_cita=hora, estado=estado, motivo=motivo)
        cita(maria, 0, time(8, 0), "Confirmada", "Limpieza dental")
        cita(luis, 0, time(9, 0), "Confirmada", "Control de ortodoncia")
        cita(rosa, 0, time(10, 30), "Programada", "Consulta por dolor molar")
        cita(carlos, 0, time(12, 0), "Programada", "Extracción")
        cita(ana, 0, time(15, 0), "Atendida", "Endodoncia (sesión 4)")
        cita(jorge, 0, time(16, 30), "Cancelada", "Blanqueamiento")
        cita(maria, 1, time(9, 0), "Programada", "Control")
        cita(rosa, 2, time(11, 0), "Confirmada", "Tratamiento de conducto")

        endodoncia = Tratamiento.objects.create(paciente=ana, tipo="Endodoncia (pieza 36)", costo_total=Decimal("1200.00"), num_sesiones=6, fecha_inicio=hoy -timedelta(days=30))

        for numero, obs in enumerate(["Apertura cameral.", "Conductometría.", "Instrumentación de conductos."], start=1):
            SesionTratamiento.objects.create(tratamiento=endodoncia, numero_sesion=numero, fecha_sesion=hoy - timedelta(days=30 - numero * 7), observaciones=obs)

        Pago.objects.create(tratamiento=endodoncia, monto=Decimal("400.00"), metodo_pago="Efectivo", fecha_pago=hoy - timedelta(days=30))
        Pago.objects.create(tratamiento=endodoncia, monto=Decimal("350.00"), metodo_pago="Yape", fecha_pago=hoy - timedelta(days=14))

        ortodoncia = Tratamiento.objects.create(paciente=luis, tipo="Ortodoncia", costo_total=Decimal("2400.00"), num_sesiones=12, fecha_inicio=hoy - timedelta(days=60))

        for numero in (1, 2):
            SesionTratamiento.objects.create(tratamiento=ortodoncia, numero_sesion=numero, fecha_sesion=hoy - timedelta(days=60 - numero * 14), observaciones="Control de brackets.")

        Pago.objects.create(tratamiento=ortodoncia, monto=Decimal("600.00"), metodo_pago="Transferencia", fecha_pago=hoy - timedelta(days=60))
        self.stdout.write(self.style.SUCCESS("Datos de prueba cargados: 6 pacientes, 8 citas, 2 tratamientos y 3 pagos."))
