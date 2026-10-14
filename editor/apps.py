from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EditorConfig(AppConfig):
    name = "editor"
    verbose_name = _("Editor")

    def ready(self):
        from . import signals  # noqa: F401
