# Define aquí tus modelos (Ticket, Comment) según los requisitos del enunciado.
# Sugerencia:
# class Ticket(models.Model): ...
# class Comment(models.Model): ...

from django.db import models

class Ticket(models.Model):
    class Priority(models.TextChoices):
        LOW = "baja", "Baja"
        MEDIUM = "media", "Media"
        HIGH = "alta", "Alta"

    class Status(models.TextChoices):
        NEW = "nuevo", "Nuevo"
        IN_PROGRESS = "en_proceso", "En Proceso"
        RESOLVED = "resuelto", "Resuelto"
        CLOSED = "cerrado", "Cerrado"

    title = models.CharField(max_length=150)
    description = models.TextField()
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    reporter_name = models.CharField(max_length=120)
    reporter_email = models.EmailField(blank=True, null=True)
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.NEW
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.status}] {self.title}"


class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.CharField(max_length=120)  # no usamos auth real
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment #{self.id} on Ticket #{self.ticket_id}"
