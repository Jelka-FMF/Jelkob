from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventStreamViewSet, PatternViewSet, StateViewSet

router = DefaultRouter(trailing_slash=False)

# REST Views
router.register("patterns", PatternViewSet, basename="pattern")
router.register("state", StateViewSet, basename="state")

# Event Stream Views
router.register("events", EventStreamViewSet, basename="stream")

urlpatterns = [
    path("", include(router.urls)),
]
