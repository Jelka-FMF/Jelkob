import os
import uuid

from django.db.models import CharField, DateTimeField, FileField, JSONField, Model
from django.utils.translation import gettext_lazy as _


class UniqueFileField(FileField):
    def generate_filename(self, instance, filename):
        _, ext = os.path.splitext(filename)
        name = f"{uuid.uuid4().hex}{ext}"
        return super().generate_filename(instance, name)


class Project(Model):
    shortid = CharField(max_length=13, unique=True, editable=False, verbose_name=_("short ID"))
    longid = CharField(max_length=23, unique=True, editable=False, verbose_name=_("long ID"))

    name = CharField(max_length=255, blank=True, verbose_name=_("name"))
    description = CharField(max_length=255, blank=True, verbose_name=_("description"))
    created = DateTimeField(auto_now_add=True, verbose_name=_("created"))

    target = CharField(max_length=255, blank=True, verbose_name=_("target"))
    editor = CharField(max_length=255, blank=True, verbose_name=_("editor"))

    meta = JSONField(default=dict, verbose_name=_("meta"))
    content = UniqueFileField(upload_to="projects", verbose_name=_("content"))

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.shortid = f"_{uuid.uuid4().hex[:12]}"
            self.longid = "-".join(f"{uuid.uuid4().int % 100000:05d}" for _ in range(4))

        super().save(*args, **kwargs)
