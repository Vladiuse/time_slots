from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("is_client_account", "client_name")
    search_fields = ("username", "client_account__client__name")

    def get_queryset(self, request: HttpRequest) -> QuerySet[User]:
        return super().get_queryset(request).select_related("client_account__client")

    @admin.display(description="Клиент", boolean=False)
    def client_name(self, user: User) -> str:
        account = getattr(user, "client_account", None)
        if account is None:
            return "—"
        return account.client.name

    @admin.display(description="Клиентский аккаунт", boolean=True)
    def is_client_account(self, user: User) -> bool:
        return hasattr(user, "client_account")
