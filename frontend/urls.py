from django.urls import path

from .views import AboutView, ManifestView, PatternsView

urlpatterns = [
    path("", PatternsView.as_view(), name="patterns"),
    path("about/", AboutView.as_view(), name="about"),
    path("site.webmanifest", ManifestView.as_view(), name="manifest"),
]
