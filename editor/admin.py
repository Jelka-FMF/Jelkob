from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "url")

    search_fields = ("name", "description")
    readonly_fields = ("shortid", "longid", "created", "content", "url")

    fieldsets = (
        (None, {"fields": ("name", "description", "created", "content", "url")}),
        (_("Identifier Information"), {"fields": ("shortid", "longid")}),
        (_("Environment Information"), {"fields": ("target", "editor")}),
    )

    @admin.display(description="URL")
    def url(self, obj):
        if not obj.pk:
            return "-"

        url = reverse("project-share-longid", kwargs={"longid": obj.longid})
        return format_html('<a href="{url}" target="_blank">' + _("Open") + "</a>", url=url)
