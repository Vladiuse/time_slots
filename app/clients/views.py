from containers.models import Container
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, OuterRef, Q, Subquery
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Client, ClientAccount


class ClientListView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        master_username = ClientAccount.objects.filter(
            client=OuterRef("pk"),
            role=ClientAccount.Role.MASTER,
        ).values("user__username")[:1]

        clients = Client.objects.annotate(
            containers_on_station=Count(
                "containers",
                filter=Q(containers__status=Container.Status.ON_STATION),
            ),
            containers_in_booking=Count(
                "containers",
                filter=Q(containers__status=Container.Status.IN_BOOKING),
            ),
            master_username=Subquery(master_username),
        ).order_by("name")
        return render(request, "clients/client_list.html", {"clients": clients})
