from django.http import HttpRequest, HttpResponse
from django.views import View


class BookingCreateView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        slot_id = request.POST.get("slot_id")
        container_numbers = request.POST.getlist("container_numbers")
        return HttpResponse(f"slot_id={slot_id}, containers={container_numbers}")
