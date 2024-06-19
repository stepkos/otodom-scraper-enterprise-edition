from django.contrib import admin

from modules.apartments.models import Apartment, ApartmentDetails


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = "title", "address", "price"
    list_filter = "rooms", "floor", "status"
    search_fields = "title", "address", "id"
    ordering = ("price",)
    readonly_fields = "subpage", "created_at", "updated_at"


admin.site.register(ApartmentDetails)
