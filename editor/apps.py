from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EditorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "editor"
    verbose_name = _("Editor")
