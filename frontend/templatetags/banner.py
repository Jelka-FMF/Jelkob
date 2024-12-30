import random

from django import template
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.simple_tag
def banner():
    banners = [
        {"src": static("frontend/banners/lights.png"), "alt": _("Christmas Lights Banner")},
        {"src": static("frontend/banners/baubles.png"), "alt": _("Christmas Baubles Banner")},
    ]
    return random.choice(banners)
