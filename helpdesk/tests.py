from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Ticket

class TicketAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ticket = Ticket.objects.create(
            title="Error de prueba",
            description="Pantalla azul",
            priority=Ticket.Priority.HIGH,
            reporter_name="Tester0",
            reporter_email="tester0@gmail.com",
        )

    def test_create_ticket(self):
        data = {
            "title": "Nuevo ticket",
            "description": "Descripción del ticket",
            "priority": "media",
            "reporter_name": "Juan0",
            "reporter_email": "juan0@gmail.com",
        }
        r = self.client.post("/api/tickets/", data, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 2)

    def test_valid_transition(self):
        r = self.client.post(
            f"/api/tickets/{self.ticket.id}/transition/",
            {"next_status": "en_proceso"},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, Ticket.Status.IN_PROGRESS)

    def test_invalid_transition(self):
        r = self.client.post(
            f"/api/tickets/{self.ticket.id}/transition/",
            {"next_status": "resuelto"},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
