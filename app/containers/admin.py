from django.contrib import admin

from containers.models import Container


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ("number", "client_name", "start_date", "end_date", "area")
    search_fields = ("number", "client_name", "send_number")
    list_filter = ("area",)
    readonly_fields = ("number",)
