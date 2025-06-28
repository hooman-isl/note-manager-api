import textwrap
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from safe_filefield.models import SafeFileField
from note.utils import generate_upload_path


class Status(models.TextChoices):
    """
    Defines the visibility status of a note.
    
    - PRIVATE: The note is visible only to the owner.
    - PUBLIC: The note is visible to others (e.g., shared or published).
    """
    PRIVATE = "PV", _("Private")
    PUBLIC = "PB", _("Public")


class Proirity(models.IntegerChoices):
    """
    Represents the priority level of a note.
    
    - LOW: Low importance.
    - MEDIUM: Normal/default importance.
    - HIGH: High importance or urgency.
    """
    LOW = 1, _("Low")
    MEDIUM  = 2, _("Medium")
    HIGH = 3, _("High")


class Note(models.Model):
    """
    Represents a personal note created by a user.

    Each note includes a title, description, tags, status (public/private),
    and a priority level. Notes can also be marked as pinned or archived.
    The creation and last edited timestamps are automatically recorded.
    """
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
        """
        Returns a shortened title preview along with the author's identity.
        Useful for admin and debugging representations.
        """
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
            ),  # Ensures only defined status values are allowed
            models.CheckConstraint(
                check=models.Q(priority__gte=Proirity.LOW, priority__lte=Proirity.HIGH),
                name="valid_priority_range"
            )   # Ensures priority is within defined integer choices
        ]


class NoteFile(models.Model):
    """
    Represents a file attached to a note.
    
    Each file is associated with a single note and stored using a secure file field.
    """
    note = models.ForeignKey(Note, on_delete=models.CASCADE, verbose_name=_("Note"))
    file = SafeFileField(upload_to=generate_upload_path, verbose_name=_("File"))

    class Meta:
        verbose_name = _("Note File")
        verbose_name_plural = _("Note Files")