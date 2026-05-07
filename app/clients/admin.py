from django.contrib import admin

from clients.models import Client, ClientAccount


class ClientAccountInline(admin.TabularInline):
    model = ClientAccount
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "source_name", "contact_full_name", "phone", "email", "is_blocked")
    search_fields = ("name", "source_name", "contact_full_name", "email")
    list_filter = ("is_blocked",)
    inlines = (ClientAccountInline,)
    fieldsets = (
        (None, {"fields": ("name", "source_name", "is_blocked")}),
        ("Контакты", {"fields": ("contact_full_name", "phone", "email", "address")}),
    )


@admin.register(ClientAccount)
class ClientAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "client", "role")
    search_fields = ("user__username", "client__name")
    list_filter = ("role",)
    autocomplete_fields = ("client",)
