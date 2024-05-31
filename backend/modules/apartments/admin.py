from django.contrib import admin
from modules.apartments.models import Apartment


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = "title", "address", "price"
    list_filter = "rooms", "floor"
    search_fields = "title", "address"
    ordering = ("price",)
    readonly_fields = "subpage", "created_at", "updated_at"
    # fields = ...
