from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import Ticket, Comment
from .serializers import TicketSerializer, CommentSerializer, TransitionSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["status", "priority"]
    search_fields = ["title"]

    @action(detail=True, methods=["post"], url_path="transition")
    def transition(self, request, pk=None):
        ticket = self.get_object()
        ser = TransitionSerializer(data=request.data, context={"ticket": ticket})
        ser.is_valid(raise_exception=True)
        ticket.status = ser.validated_data["next_status"]
        ticket.save(update_fields=["status", "updated_at"])
        return Response(TicketSerializer(ticket).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="comments")
    def add_comment(self, request, pk=None):
        ticket = self.get_object()
        payload = {
            "ticket": ticket.id,
            "author": request.data.get("author") or "anon",
            "text": (request.data.get("text") or "").strip(),
        }
        cser = CommentSerializer(data=payload)
        cser.is_valid(raise_exception=True)
        cser.save()
        return Response(cser.data, status=status.HTTP_201_CREATED)

class CommentViewSet(mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Comment.objects.all()
        ticket_id = self.request.query_params.get("ticket")
        if ticket_id:
            qs = qs.filter(ticket_id=ticket_id)
        return qs
