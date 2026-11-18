"""Envía por correo el recordatorio de las citas de mañana (RF-07).

Uso:  python manage.py enviar_recordatorios
Se programa una vez al día con el Programador de tareas de Windows.
"""
from datetime import timedelta

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from citas.models import Cita, ESTADOS_VIGENTES

class Command(BaseCommand):
    help = "Envía el recordatorio por correo de las citas vigentes de mañana."

    def handle(self, *args, **opciones):
        manana = timezone.localdate() + timedelta(days=1)
        pendientes = Cita.objects.filter(fecha_cita=manana, estado__in=ESTADOS_VIGENTES, recordatorio_enviado=False).select_related("paciente")
        enviados = 0
        for cita in pendientes:
            if not cita.paciente.correo:                  # sin correo no hay a quién avisar
                continue
            send_mail(
                subject="Recordatorio de su cita - Consultorio NADINNE",
                message=("Hola %s,\n\nLe recordamos su cita el %s a las %s.\n" "Si no puede asistir, comuníquese con el consultorio.\n\nConsultorio Odontológico NADINNE")
                        % (cita.paciente.nombres, cita.fecha_cita.strftime("%d/%m/%Y"), cita.hora_cita.strftime("%H:%M")),
                from_email=None, recipient_list=[cita.paciente.correo])
            cita.recordatorio_enviado = True              # evita avisar dos veces
            cita.save(update_fields=["recordatorio_enviado"])
            enviados += 1
        self.stdout.write(self.style.SUCCESS("Recordatorios enviados: %d" % enviados))

