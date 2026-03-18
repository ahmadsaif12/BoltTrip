from django.urls import path

from .views import BookingPaymentViewSet, BookingTravelerViewSet, BookingViewSet

urlpatterns = [
    path(
        "",
        BookingViewSet.as_view({"get": "list", "post": "create"}),
        name="booking-list",
    ),
    path(
        "<int:pk>/",
        BookingViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        name="booking-detail",
    ),
    path(
        "travelers/",
        BookingTravelerViewSet.as_view({"get": "list", "post": "create"}),
        name="booking-traveler-list",
    ),
    path(
        "travelers/<int:pk>/",
        BookingTravelerViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        name="booking-traveler-detail",
    ),
    path(
        "payments/",
        BookingPaymentViewSet.as_view({"get": "list", "post": "create"}),
        name="booking-payment-list",
    ),
    path(
        "payments/<int:pk>/",
        BookingPaymentViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        name="booking-payment-detail",
    ),
]
