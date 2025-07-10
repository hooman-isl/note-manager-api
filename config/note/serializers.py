from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from taggit.serializers import TaggitSerializer, TagListSerializerField
from note.models import *
from note import app_settings


class NoteSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field=get_user_model().USERNAME_FIELD, read_only=True
    )
    files = serializers.SerializerMethodField()
    tags = TagListSerializerField(label=_("Tags"))

    def get_files(self, note):
        return reverse(
            viewname="notefile-list", args=[note.pk], request=self.context["request"]
        )

    class Meta:
        model = Note
        fields = "__all__"
        extra_kwargs = {
            datetime_field: {"format": app_settings.DATETIME_FORMAT}
            for datetime_field in ("created_at", "edited_at")
        }


class NoteFileSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'note_pk': 'note__pk'
    }

    class Meta:
        model = NoteFile
        fields = "__all__"