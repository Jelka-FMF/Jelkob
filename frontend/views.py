from django.http import JsonResponse
from django.templatetags.static import static
from django.views import View
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _


class PatternsView(TemplateView):
    template_name = "frontend/patterns.html"


class AboutView(TemplateView):
    template_name = "frontend/about.html"


class ContactView(TemplateView):
    template_name = "frontend/contact.html"


class ManifestView(View):
    @staticmethod
    def get(request):
        manifest = {
            "name": "Jelka FMF",
            "description": _(
                "Christmas tree at the Faculty of Mathematics and Physics, University of Ljubljana"
            ),
            "display": "standalone",
            "theme_color": "#0a0c0d",
            "start_url": "/",
            "scope": "/",
            "icons": [
                {
                    "src": static("frontend/icons/favicon.svg"),
                    "type": "image/svg+xml",
                    "sizes": "any",
                },
                {
                    "src": static("frontend/icons/favicon-maskable.svg"),
                    "type": "image/svg+xml",
                    "sizes": "any",
                    "purpose": "maskable",
                },
                {
                    "src": static("frontend/icons/favicon-monochrome.svg"),
                    "type": "image/svg+xml",
                    "sizes": "any",
                    "purpose": "monochrome",
                },
            ],
        }

        return JsonResponse(manifest, content_type="application/manifest+json")
