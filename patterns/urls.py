from django.urls import include, path
from rest_framework.routers import DefaultRouter

from patterns.views import PatternViewSet

router = DefaultRouter()
router.register("", PatternViewSet, basename="pattern")

urlpatterns = [
    path("", include(router.urls)),
]
