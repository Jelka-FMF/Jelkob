from django.views.generic import TemplateView

from runner.models import Pattern


class PatternsView(TemplateView):
    template_name = "frontend/patterns.html"


class AboutView(TemplateView):
    template_name = "frontend/about.html"
