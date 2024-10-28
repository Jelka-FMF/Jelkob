from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class Pattern(models.Model):
    identifier = models.CharField(max_length=50, unique=True, verbose_name=_("identifier"))
    name = models.CharField(max_length=255, verbose_name=_("name"))
    docker = models.CharField(max_length=255, verbose_name=_("docker"))
    duration = models.IntegerField(blank=True, null=True, verbose_name=_("duration"))
    author = models.CharField(max_length=255, blank=True, verbose_name=_("author"))
    school = models.CharField(max_length=255, blank=True, verbose_name=_("school"))
    enabled = models.BooleanField(default=True, verbose_name=_("enabled"))

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("pattern")
        verbose_name_plural = _("patterns")

    def __str__(self):
        return self.name
