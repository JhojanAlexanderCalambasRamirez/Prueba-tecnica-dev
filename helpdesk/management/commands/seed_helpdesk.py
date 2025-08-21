from django.core.management.base import BaseCommand
from helpdesk.models import Ticket, Comment

class Command(BaseCommand):
    help = "Crea tickets y comentarios de ejemplo"

    def handle(self, *args, **kwargs):
        Comment.objects.all().delete()
        Ticket.objects.all().delete()

        t1 = Ticket.objects.create(
            title="No puedo acceder al sistema",
            description="Pantalla en blanco al iniciar sesión.",
            priority=Ticket.Priority.HIGH,
            reporter_name="Laura0",
            reporter_email="laura0@gmail.com",
        )
        t2 = Ticket.objects.create(
            title="Mejora: exportar reportes a CSV",
            description="Agregar botón de exportación en pantalla de reportes.",
            priority=Ticket.Priority.MEDIUM,
            reporter_name="Carlos0",
            reporter_email="carlos0@gmail.com",
        )
        t3 = Ticket.objects.create(
            title="Bug en reporte mensual",
            description="Valores inconsistentes en totales.",
            priority=Ticket.Priority.LOW,
            reporter_name="Ana",
            status=Ticket.Status.IN_PROGRESS,
        )

        Comment.objects.bulk_create([
            Comment(ticket=t1, author="Soporte", text="Revisando logs del servidor."),
            Comment(ticket=t1, author="Laura", text="Sigue ocurriendo luego de reiniciar."),
            Comment(ticket=t3, author="Soporte", text="Bug reproducido, preparando fix."),
        ])

        self.stdout.write(self.style.SUCCESS("Datos de ejemplo creados"))
