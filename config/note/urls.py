from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter
from note import views


router = SimpleRouter()
router.register("notes", views.NoteAPIView, basename="note")

nested_router = NestedSimpleRouter(router, "notes", lookup="note")
nested_router.register("files", views.NoteFileAPIView, basename="notefile")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(nested_router.urls)),
]