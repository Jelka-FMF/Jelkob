from datetime import datetime

from django.conf import settings
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
    current_pattern = ForeignKey(Pattern, on_delete=SET_NULL, blank=True, null=True, verbose_name=_("current pattern"))  # fmt: skip
    current_pattern_started = DateTimeField(blank=True, null=True, verbose_name=_("current pattern started"))

    runner_last_active = DateTimeField(blank=True, null=True, verbose_name=_("runner last active"))

    class Meta:
        verbose_name = _("state")

    def __str__(self):
        return gettext("State")

    @property
    def current_pattern_remaining(self):
        if not self.current_pattern or not self.current_pattern_started:
            return 0.0

        duration = self.current_pattern.duration or Config.get_solo().default_duration
        started = self.current_pattern_started.timestamp()
        now = datetime.now().timestamp()

        return max(0.0, duration - (now - started))

    @property
    def runner_is_active(self):
        # Runner cannot be active if it is not running any pattern
        if not self.current_pattern or not self.current_pattern_started:
            return False

        # Runner cannot be active if it has not pinged the server yet
        if not self.runner_last_active:
            return False

        # Runner cannot be active if it has not pinged the server in a specific time frame
        if (
            datetime.now().timestamp() - self.runner_last_active.timestamp()
            >= settings.INACTIVITY_PING_TIMEOUT
        ):
            return False

        # Runner cannot be active if a new pattern has not started in a specific time frame
        if (
            datetime.now().timestamp()
            - self.current_pattern_started.timestamp()
            - (self.current_pattern.duration or Config.get_solo().default_duration)
            >= settings.INACTIVITY_PATTERN_TIMEOUT
        ):
            return False

        return True


class Config(SingletonModel):
    default_duration = PositiveIntegerField(default=60, verbose_name=_("default duration"))

    class Meta:
        verbose_name = _("config")

    def __str__(self):
        return gettext("Config")
