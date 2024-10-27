from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Pattern


@admin.register(Pattern)
class PatternAdmin(SimpleHistoryAdmin):
    list_display = ("identifier", "name", "container", "duration", "author", "school", "enabled")
    list_filter = ("enabled",)
