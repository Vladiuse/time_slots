from clients.models import Client
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Container


def containers_list(request: HttpRequest) -> HttpResponse:
    client = Client.objects.get(source_name='ООО "КРАФТТРАНС"')
    containers = Container.objects.filter(client=client)
    content = {
        "containers": containers,
        "status_on_station": Container.Status.ON_STATION,
    }
    return render(request, "containers/container_list.html", content)
