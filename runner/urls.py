from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ControlEventsViewSet, PatternViewSet, StateViewSet, StatusEventsViewSet

router = DefaultRouter(trailing_slash=False)

# REST Views
router.register("patterns", PatternViewSet, basename="pattern")
router.register("state", StateViewSet, basename="state")

# Event Stream Views
router.register("events/control", ControlEventsViewSet, basename="events-control")
router.register("events/status", StatusEventsViewSet, basename="events-status")

urlpatterns = [
    path("", include(router.urls)),
]
