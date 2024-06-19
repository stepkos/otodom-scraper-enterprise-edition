from django.contrib import admin

from modules.core.models import CeleryResult


@admin.register(CeleryResult)
class CeleryResultAdmin(admin.ModelAdmin):
    list_display = "task_name", "task_id", "is_success", "created_at"
    readonly_fields = "created_at", "updated_at"
    search_fields = "task_name", "task_id", "created_at"
    ordering = ("created_at",)
