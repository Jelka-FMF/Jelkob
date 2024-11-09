from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Index,
    Model,
    PositiveIntegerField,
    SET_NULL,
    URLField,
)
from django.utils.translation import gettext, gettext_lazy as _
from simple_history.models import HistoricalRecords
from solo.models import SingletonModel


class Pattern(Model):
    # Base Information
    identifier = CharField(max_length=50, unique=True, verbose_name=_("identifier"))
    name = CharField(max_length=50, verbose_name=_("name"))
    description = CharField(max_length=200, blank=True, verbose_name=_("description"))
    source = URLField(max_length=200, blank=True, verbose_name=_("source"))

    # Runner Information
    docker = CharField(max_length=200, verbose_name=_("docker"))
    duration = PositiveIntegerField(blank=True, null=True, verbose_name=_("duration"))

    # Author Information
    author = CharField(max_length=50, blank=True, verbose_name=_("author"))
    school = CharField(max_length=100, blank=True, verbose_name=_("school"))

    # Pattern Status
    enabled = BooleanField(default=True, verbose_name=_("enabled"))
    visible = BooleanField(default=True, verbose_name=_("visible"))

    # Pattern History
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("pattern")
        verbose_name_plural = _("patterns")

        ordering = ["identifier"]

        indexes = [
            Index(fields=["identifier"]),
        ]

    def __str__(self):
        return self.name


class State(SingletonModel):
    pattern = ForeignKey(Pattern, on_delete=SET_NULL, blank=True, null=True, verbose_name=_("pattern"))
    started = DateTimeField(blank=True, null=True, verbose_name=_("start time"))
    active = DateTimeField(blank=True, null=True, verbose_name=_("active time"))

    class Meta:
        verbose_name = _("state")

    def __str__(self):
        return gettext("State")


class Config(SingletonModel):
    duration = PositiveIntegerField(default=60, verbose_name=_("default duration"))

    class Meta:
        verbose_name = _("config")

    def __str__(self):
        return gettext("Config")
