from functools import wraps
from django.db.models import QuerySet
from rest_framework.response import Response


def paginated_response(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        queryset = func(self, *args, **kwargs)

        assert isinstance(queryset, (list, QuerySet)), (
            f"@paginated_response decorator expected {func.__name__} "
            f"to return a list or QuerySet, got {type(queryset).__name__}"
        )

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)

    return wrapped