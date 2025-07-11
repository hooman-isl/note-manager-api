from functools import wraps
from django.db.models import QuerySet
from rest_framework.response import Response


def paginated_response(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        queryset = func(self, *args, **kwargs)

        assert isinstance(queryset, (list, QuerySet)), (
            f"{self.__class__.__name__}.{func.__name__} "
            f"should return a QuerySet or list, not {type(queryset).__name__!r}"
        )

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)

    return wrapped