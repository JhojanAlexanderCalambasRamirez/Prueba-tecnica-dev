from django.contrib import admin
from .models import Ticket, Comment

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "priority", "status", "reporter_name", "created_at")
    list_filter = ("priority", "status", "created_at")
    search_fields = ("title", "description", "reporter_name", "reporter_email")
    ordering = ("-created_at",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "author", "created_at")
    list_filter = ("created_at", "author")
    search_fields = ("text", "author")
    ordering = ("-created_at",)
