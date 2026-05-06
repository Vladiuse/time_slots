from django.contrib import admin

from bookings.models import Booking, Slot


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ("date", "start_time", "end_time", "current_count", "container_limit", "is_blocked")
    list_filter = ("is_blocked", "date")
    search_fields = ("date",)
    ordering = ("-date", "start_time")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("container", "slot", "status", "created_at")
    list_filter = ("status", "slot__date")
    search_fields = ("container__number",)
    ordering = ("-created_at",)
    autocomplete_fields = ("container", "slot")
