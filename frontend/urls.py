from django.urls import path

from .views import AboutView, PatternsView

urlpatterns = [
    path("", PatternsView.as_view(), name="patterns"),
    path("about/", AboutView.as_view(), name="about"),
]
