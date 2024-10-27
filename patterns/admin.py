from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Pattern


@admin.register(Pattern)
class PatternAdmin(SimpleHistoryAdmin):
    list_display = ("identifier", "name", "image", "duration", "author", "school", "enabled")
    list_filter = ("enabled",)

    actions = ("enable", "disable")

    @admin.action(description="Enable selected patterns")
    def enable(self, request, queryset):
        queryset.update(enabled=True)

    @admin.action(description="Disable selected patterns")
    def disable(self, request, queryset):
        queryset.update(enabled=False)
