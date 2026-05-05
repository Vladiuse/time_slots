from django.contrib import admin

from containers.models import Container


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("client", "number", "client_name", "status", "start_date", "end_date", "area")
    search_fields = ("number", "client_name", "send_number")
    list_filter = ("status", "area")
    readonly_fields = ("number",)
