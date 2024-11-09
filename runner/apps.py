from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RunnerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "runner"
    verbose_name = _("Runner")

    def ready(self):
        from . import signals  # noqa: F401
