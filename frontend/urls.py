from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView

from .views import AboutView, ContactView, InteractionView, ManifestView, PatternsView

urlpatterns = [
    path("", PatternsView.as_view(), name="patterns"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("interaction/", InteractionView.as_view(), name="interaction"),
    path("site.webmanifest", ManifestView.as_view(), name="manifest"),
    path("favicon.ico", RedirectView.as_view(url=static("frontend/icons/favicon.ico"), permanent=True)),
]
