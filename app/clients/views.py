from containers.models import Container
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Client


class ClientListView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        clients = Client.objects.annotate(
            containers_on_station=Count(
                "containers",
                filter=Q(containers__status=Container.Status.ON_STATION),
            ),
            containers_in_booking=Count(
                "containers",
                filter=Q(containers__status=Container.Status.IN_BOOKING),
            ),
        ).order_by("name")
        return render(request, "clients/client_list.html", {"clients": clients})
