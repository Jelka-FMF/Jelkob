import os
import uuid

from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    FileField,
    ForeignKey,
    Index,
    JSONField,
    Model,
    PROTECT,
    PositiveIntegerField,
)
from django.utils.translation import gettext_lazy as _


class UniqueFileField(FileField):
    def generate_filename(self, instance, filename):
        _, ext = os.path.splitext(filename)
        name = f"{uuid.uuid4().hex}{ext}"
        return super().generate_filename(instance, name)


class Project(Model):
    # Identifier Information
    shortid = CharField(max_length=13, unique=True, editable=False, verbose_name=_("short ID"))
    longid = CharField(max_length=23, unique=True, editable=False, verbose_name=_("long ID"))

    # Base Information
    name = CharField(max_length=50, blank=True, verbose_name=_("name"))
    description = CharField(max_length=200, blank=True, verbose_name=_("description"))
    created = DateTimeField(auto_now_add=True, verbose_name=_("created"))

    # Environment Information
    target = CharField(max_length=50, blank=True, verbose_name=_("target"))
    editor = CharField(max_length=50, blank=True, verbose_name=_("editor"))

    # Content Information
    meta = JSONField(default=dict, verbose_name=_("meta"))
    content = UniqueFileField(upload_to="projects", verbose_name=_("content"))

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")

        indexes = [
            Index(fields=["shortid"]),
            Index(fields=["longid"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.shortid = f"_{uuid.uuid4().hex[:12]}"
            self.longid = "-".join(f"{uuid.uuid4().int % 100000:05d}" for _ in range(4))

        super().save(*args, **kwargs)


class Submission(Model):
    # Base Information
    name = CharField(max_length=50, blank=True, verbose_name=_("name"))
    description = CharField(max_length=200, blank=True, verbose_name=_("description"))

    # Runner Information
    duration = PositiveIntegerField(blank=True, null=True, verbose_name=_("duration"))

    # Author Information
    author = CharField(max_length=50, blank=True, verbose_name=_("author"))
    school = CharField(max_length=100, blank=True, verbose_name=_("school"))

    # Submission Status
    reviewed = BooleanField(default=False, verbose_name=_("reviewed"))
    approved = BooleanField(blank=True, null=True, verbose_name=_("approved"))

    # Submission Content
    project = ForeignKey(Project, on_delete=PROTECT, related_name="submissions", verbose_name=_("project"))

    class Meta:
        verbose_name = _("submission")
        verbose_name_plural = _("submissions")

    def __str__(self):
        return self.name
