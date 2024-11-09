from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin
from solo.admin import SingletonModelAdmin

from .models import Config, Pattern, State


@admin.register(Pattern)
class PatternAdmin(SimpleHistoryAdmin):
    list_display = ("identifier", "name", "duration", "author", "school", "enabled", "visible")
    list_filter = ("enabled", "visible", "author", "school")

    search_fields = ("identifier", "name", "docker", "author", "school")

    fieldsets = (
        (None, {"fields": ("identifier", "name", "description", "source")}),
        (_("Runner Information"), {"fields": ("docker", "duration")}),
        (_("Author Information"), {"fields": ("author", "school")}),
        (_("Pattern Status"), {"fields": ("enabled", "visible")}),
    )

    actions = ("enable", "disable")

    @admin.action(description=_("Enable selected patterns"))
    def enable(self, request, queryset):
        queryset.update(enabled=True)

    @admin.action(description=_("Disable selected patterns"))
    def disable(self, request, queryset):
        queryset.update(enabled=False)

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions["delete_selected"][0].short_description = _("Delete selected patterns")
        return actions


@admin.register(State)
class StateAdmin(SingletonModelAdmin):
    pass


@admin.register(Config)
class ConfigAdmin(SingletonModelAdmin):
    pass
