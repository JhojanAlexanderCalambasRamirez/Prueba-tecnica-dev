from rest_framework import serializers
from .models import Ticket, Comment

VALID_TRANSITIONS = {
    Ticket.Status.NEW: {Ticket.Status.IN_PROGRESS},
    Ticket.Status.IN_PROGRESS: {Ticket.Status.NEW, Ticket.Status.RESOLVED},
    Ticket.Status.RESOLVED: {Ticket.Status.CLOSED},
    Ticket.Status.CLOSED: set(),
}

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "ticket", "author", "text", "created_at"]
        read_only_fields = ["id", "created_at"]

class TicketSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id", "title", "description", "priority",
            "reporter_name", "reporter_email", "status",
            "created_at", "updated_at", "comments",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

class TransitionSerializer(serializers.Serializer):
    next_status = serializers.ChoiceField(choices=Ticket.Status.choices)

    def validate(self, attrs):
        ticket = self.context["ticket"]
        nxt = attrs["next_status"]
        if nxt not in VALID_TRANSITIONS[ticket.status]:
            raise serializers.ValidationError(
                {"detail": f"Transición inválida: {ticket.status} → {nxt}"}
            )
        return attrs
