import textwrap
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from safe_filefield.models import SafeFileField
from note.utils import generate_upload_path


class Status(models.TextChoices):
    PRIVATE = "PV", _("Private")
    PUBLIC = "PB", _("Public")


class Proirity(models.IntegerChoices):
    LOW = 1, _("Low")
    MEDIUM  = 2, _("Medium")
    HIGH = 3, _("High")


class Note(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("User"))
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))
    status = models.CharField(_("Status"), choices=Status.choices, default=Status.PUBLIC, max_length=2)
    priority = models.SmallIntegerField(_("Priority"), choices=Proirity.choices, default=Proirity.MEDIUM)
    is_archived = models.BooleanField(_("Archived"), default=False)
    is_pinned = models.BooleanField(_("Pinned"), default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    edited_at = models.DateTimeField(_("Edited At"), auto_now=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return (
            f"'{textwrap.shorten(self.title, width=50, placeholder="...")}' from {self.user}"
        )

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")
        constraints = [
            models.CheckConstraint(
                check=models.Q(status__in=[Status.PRIVATE, Status.PUBLIC]),
                name="valid_status_choices"
            ),
            models.CheckConstraint(
                check=models.Q(priority__gte=Proirity.LOW, priority__lte=Proirity.HIGH),
                name="valid_priority_range"
            )
        ]


class NoteFile(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, verbose_name=_("Note"))
    file = SafeFileField(upload_to=generate_upload_path, verbose_name=_("File"))

    def __str__(self):
        return f"File for '{self.note}': {self.file.name}"

    class Meta:
        verbose_name = _("Note File")
        verbose_name_plural = _("Note Files")


class NoteReminder(models.Model):
    note = models.OneToOneField(Note, on_delete=models.CASCADE, verbose_name=_("Note"))
    due_date = models.DateTimeField(_("Due Date"))
    is_active = models.BooleanField(_("Activated"), default=False)

    def __str__(self):
        return f"Reminder for '{self.note}'"

    class Meta:
        verbose_name = _("Note Reminder")
        verbose_name_plural = _("Note Reminders")