from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PatternViewSet, StateViewSet

router = DefaultRouter(trailing_slash=False)
router.register("patterns", PatternViewSet, basename="pattern")
router.register("state", StateViewSet, basename="state")

urlpatterns = [
    path("api/", include(router.urls)),
]
