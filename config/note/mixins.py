from rest_framework import permissions


class AuthenticatedUserMixin:
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        self.auth_user = request.user
        return super().dispatch(request, *args, **kwargs)