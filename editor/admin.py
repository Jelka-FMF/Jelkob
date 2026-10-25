from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import formats, timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import PXTProject, PythonProject, Submission

PROJECT_TYPE_LABELS = {
    PXTProject: _("Jelkly"),
    PythonProject: _("Jelkonda"),
}


class ProjectTypeFilter(admin.SimpleListFilter):
    title = _("type")
    parameter_name = "type"

    models = {
        "pxt": PXTProject,
        "python": PythonProject,
    }

    def lookups(self, request, model_admin):
        return [(key, PROJECT_TYPE_LABELS[model]) for key, model in self.models.items()]

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset

        model = self.models.get(value)
        if model is None:
            return queryset

        ctype = ContentType.objects.get_for_model(model)
        return queryset.filter(project__polymorphic_ctype=ctype)


@admin.register(PXTProject)
class PXTProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "url")

    search_fields = ("name", "description")
    readonly_fields = ("ulid", "shortid", "longid", "created", "url")

    fieldsets = (
        (None, {"fields": ("name", "description", "created", "url")}),
        (_("Identifier Information"), {"fields": ("ulid", "shortid", "longid")}),
        (_("Environment Information"), {"fields": ("target", "editor")}),
        (_("Content Information"), {"fields": ("meta", "content")}),
    )

    @admin.display(description=_("URL"))
    def url(self, obj):
        if not obj.pk:
            return "-"

        url = reverse("project-share", kwargs={"ulid": obj.ulid})
        return format_html('<a href="{url}" target="_blank">' + _("Open") + "</a>", url=url)


@admin.register(PythonProject)
class PythonProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "url")

    search_fields = ("name", "description")
    readonly_fields = ("ulid", "created", "url")

    fieldsets = (
        (None, {"fields": ("name", "description", "created", "url")}),
        (_("Identifier Information"), {"fields": ("ulid",)}),
        (_("Content Information"), {"fields": ("meta", "content")}),
    )

    @admin.display(description=_("URL"))
    def url(self, obj):
        if not obj.pk:
            return "-"

        url = reverse("project-share", kwargs={"ulid": obj.ulid})
        return format_html('<a href="{url}" target="_blank">' + _("Open") + "</a>", url=url)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "duration", "author", "school", "created", "url", "reviewed", "approved")
    list_filter = (ProjectTypeFilter, "reviewed", "approved", "school", "author")

    search_fields = ("name", "author", "school")
    readonly_fields = ("type", "created", "url")

    fieldsets = (
        (None, {"fields": ("name", "description", "type", "created", "url")}),
        (_("Runner Information"), {"fields": ("duration",)}),
        (_("Author Information"), {"fields": ("author", "school")}),
        (_("Submission Content"), {"fields": ("project",)}),
        (_("Submission Status"), {"fields": ("reviewed", "approved")}),
    )

    @admin.display(description=_("type"))
    def type(self, obj):
        if not obj or not obj.project_id:
            return "-"

        model = obj.project.get_real_instance_class()
        return PROJECT_TYPE_LABELS[model]

    @admin.display(description=_("created"), ordering="project__created")
    def created(self, obj):
        if not obj.pk or not obj.project:
            return "-"

        return formats.localize(timezone.template_localtime(obj.project.created))

    @admin.display(description=_("URL"))
    def url(self, obj):
        if not obj.pk or not obj.project:
            return "-"

        url = reverse("project-share", kwargs={"ulid": obj.project.ulid})
        return format_html('<a href="{url}" target="_blank">' + _("Open") + "</a>", url=url)
