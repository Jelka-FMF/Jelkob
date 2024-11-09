from django.views.generic import TemplateView


class PatternsView(TemplateView):
    template_name = "frontend/patterns.html"


class AboutView(TemplateView):
    template_name = "frontend/about.html"
