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

    actions = ("enable", "disable", "show", "hide")

    @admin.action(description=_("Enable selected patterns"))
    def enable(self, request, queryset):
        queryset.update(enabled=True)

    @admin.action(description=_("Disable selected patterns"))
    def disable(self, request, queryset):
        queryset.update(enabled=False)

    @admin.action(description=_("Show selected patterns"))
    def show(self, request, queryset):
        queryset.update(visible=True)

    @admin.action(description=_("Hide selected patterns"))
    def hide(self, request, queryset):
        queryset.update(visible=False)

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions["delete_selected"][0].short_description = _("Delete selected patterns")
        return actions


@admin.register(State)
class StateAdmin(SingletonModelAdmin):
    readonly_fields = (
        "current_pattern_remaining",
        "runner_is_active",
    )

    fieldsets = (
        (
            _("Pattern Status"),
            {"fields": ("current_pattern", "current_pattern_started", "current_pattern_remaining")},
        ),
        (
            _("Runner Status"),
            {"fields": ("runner_last_active", "runner_is_active")},
        ),
    )

    @admin.display(description=_("current pattern remaining"))
    def current_pattern_remaining(self, obj):
        return obj.current_pattern_remaining

    @admin.display(description=_("runner is active"), boolean=True)
    def runner_is_active(self, obj):
        return obj.runner_is_active


@admin.register(Config)
class ConfigAdmin(SingletonModelAdmin):
    pass
