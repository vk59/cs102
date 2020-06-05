from django.contrib import admin
from .models import Note

class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "pub_date", "tags", "was_published_recently")
    list_filter = ["pub_date"]

admin.site.register(Note)
