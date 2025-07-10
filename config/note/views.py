from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework_nested.viewsets import NestedViewSetMixin
from note.serializers import *
from note.models import Note
from note.mixins import AuthenticatedUserMixin
from note.decorators import paginated_response
from rest_framework.response import Response


class NoteAPIView(AuthenticatedUserMixin, viewsets.ModelViewSet):
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(user=self.auth_user)

    def perform_create(self, serializer):
        serializer.save(user=self.auth_user)

    @paginated_response
    @action(
        detail=False, methods=["get"], serializer_class=NoteFileSerializer
    )
    def files(self, request):
        return NoteFile.objects.filter(note__user=self.auth_user)


class NoteFileAPIView(
    AuthenticatedUserMixin, NestedViewSetMixin, viewsets.ModelViewSet
):
    serializer_class = NoteFileSerializer
    queryset = NoteFile.objects.all()
    parent_lookup_kwargs = {'note_pk': 'note__pk'}
