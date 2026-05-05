from django.contrib import admin

from clients.models import Client, ClientAccount


class ClientAccountInline(admin.TabularInline):
    model = ClientAccount
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "source_name", "is_blocked")
    search_fields = ("name", "source_name")
    list_filter = ("is_blocked",)
    inlines = (ClientAccountInline,)


@admin.register(ClientAccount)
class ClientAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "client", "role")
    search_fields = ("user__username", "client__name")
    list_filter = ("role",)
