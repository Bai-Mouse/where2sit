from django.urls import path
from .views import create_reservation, reservation_page

urlpatterns = [
    path("", reservation_page, name="reservation_page"),
    path("reserve/", create_reservation),
]