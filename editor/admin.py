from django.contrib import admin
from django.urls import reverse
from django.utils import formats, timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Project, Submission


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "url")

    search_fields = ("name", "description")
    readonly_fields = ("shortid", "longid", "created", "url")

    fieldsets = (
        (None, {"fields": ("name", "description", "created", "url")}),
        (_("Identifier Information"), {"fields": ("shortid", "longid")}),
        (_("Environment Information"), {"fields": ("target", "editor")}),
        (_("Content Information"), {"fields": ("meta", "content")}),
    )

    @admin.display(description=_("URL"))
    def url(self, obj):
        if not obj.pk:
            return "-"

        url = reverse("project-share-longid", kwargs={"longid": obj.longid})
        return format_html('<a href="{url}" target="_blank">' + _("Open") + "</a>", url=url)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "duration", "author", "school", "created", "url", "reviewed", "approved")
    list_filter = ("reviewed", "approved", "author", "school")

    search_fields = ("name", "author", "school")
    readonly_fields = ("created", "url")

    fieldsets = (
        (None, {"fields": ("name", "description", "created", "url")}),
        (_("Runner Information"), {"fields": ("duration",)}),
        (_("Author Information"), {"fields": ("author", "school")}),
        (_("Submission Content"), {"fields": ("project",)}),
        (_("Submission Status"), {"fields": ("reviewed", "approved")}),
    )

    @admin.display(description=_("created"), ordering="project__created")
    def created(self, obj):
        if not obj.pk or not obj.project:
            return "-"

        return formats.localize(timezone.template_localtime(obj.project.created))

    @admin.display(description=_("URL"))
    def url(self, obj):
        if not obj.pk or not obj.project:
            return "-"

        url = reverse("project-share-longid", kwargs={"longid": obj.project.longid})
        return format_html('<a href="{url}" target="_blank">' + _("Open") + "</a>", url=url)
