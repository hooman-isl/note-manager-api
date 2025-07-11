from django.utils.translation import gettext_lazy as _
import django_filters
from note.models import Note


class NoteFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(
        lookup_expr="date", label=_("Created At (Exact Date)")
    )
    created_at__range = django_filters.DateFromToRangeFilter(
        field_name="created_at", label=_("Created At (Date Range)")
    )

    class Meta:
        model = Note
        fields = (
            "status", "priority", "is_archived", "is_pinned", "tags__name"
        )