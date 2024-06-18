from django.contrib import admin
from modules.core.models import CeleryResult


@admin.register(CeleryResult)
class CeleryResultAdmin(admin.ModelAdmin):
    list_display = "task_name", "task_id", "result"
    readonly_fields = "created_at", "updated_at"
