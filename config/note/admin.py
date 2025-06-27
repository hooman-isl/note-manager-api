from django.contrib import admin
from note.models import *


class NoteFileInline(admin.StackedInline):
    model = NoteFile
    extra = 0


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    inlines = [NoteFileInline]