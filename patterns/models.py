from django.db.models import BooleanField, CharField, DateTimeField, ForeignKey, IntegerField, Model, SET_NULL
from django.utils.translation import gettext, gettext_lazy as _
from simple_history.models import HistoricalRecords
from solo.models import SingletonModel


class Pattern(Model):
    identifier = CharField(max_length=50, unique=True, verbose_name=_("identifier"))
    name = CharField(max_length=255, verbose_name=_("name"))
    docker = CharField(max_length=255, verbose_name=_("docker"))
    duration = IntegerField(blank=True, null=True, verbose_name=_("duration"))
    author = CharField(max_length=255, blank=True, verbose_name=_("author"))
    school = CharField(max_length=255, blank=True, verbose_name=_("school"))
    enabled = BooleanField(default=True, verbose_name=_("enabled"))

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("pattern")
        verbose_name_plural = _("patterns")

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
