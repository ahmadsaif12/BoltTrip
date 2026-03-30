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
    path(
        "payments/initiate_esewa/",
        BookingPaymentViewSet.as_view({"post": "initiate_esewa"}),
        name="booking-payment-initiate-esewa",
    ),
    path(
        "payments/initiate_khalti/",
        BookingPaymentViewSet.as_view({"post": "initiate_khalti"}),
        name="booking-payment-initiate-khalti",
    ),
    path(
        "payments/verify_esewa/",
        BookingPaymentViewSet.as_view({"post": "verify_esewa"}),
        name="booking-payment-verify-esewa",
    ),
    path(
        "payments/verify_khalti/",
        BookingPaymentViewSet.as_view({"post": "verify_khalti"}),
        name="booking-payment-verify-khalti",
    ),
]
