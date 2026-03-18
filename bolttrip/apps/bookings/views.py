import uuid

from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from apps.misc.schema import (
    booking_payment_viewset_schema,
    booking_traveler_viewset_schema,
    booking_viewset_schema,
)

from .models import Booking, BookingPayment, BookingTraveler
from .serializers import (
    BookingPaymentSerializer,
    BookingPaymentWriteSerializer,
    BookingSerializer,
    BookingTravelerSerializer,
    BookingTravelerWriteSerializer,
    BookingWriteSerializer,
)


@booking_viewset_schema
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related(
        "user",
        "package",
        "hotel",
        "activity",
        "guide",
    ).prefetch_related("travelers", "payments")
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["booking_reference", "contact_name", "contact_email"]
    ordering_fields = ["start_date", "created_at", "total_amount"]

    def get_queryset(self):
        if not getattr(self.request, "user", None) or not self.request.user.is_authenticated:
            return Booking.objects.none()
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in {"create", "partial_update"}:
            return BookingWriteSerializer
        return BookingSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            booking_reference=f"BK-{uuid.uuid4().hex[:10].upper()}",
        )


@booking_traveler_viewset_schema
class BookingTravelerViewSet(viewsets.ModelViewSet):
    queryset = BookingTraveler.objects.select_related("booking", "booking__user")
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        if not getattr(self.request, "user", None) or not self.request.user.is_authenticated:
            return BookingTraveler.objects.none()
        return self.queryset.filter(booking__user=self.request.user)

    def get_serializer_class(self):
        if self.action in {"create", "partial_update"}:
            return BookingTravelerWriteSerializer
        return BookingTravelerSerializer

    def perform_create(self, serializer):
        booking = get_object_or_404(Booking, pk=self.request.data.get("booking"), user=self.request.user)
        serializer.save(booking=booking)


@booking_payment_viewset_schema
class BookingPaymentViewSet(viewsets.ModelViewSet):
    queryset = BookingPayment.objects.select_related("booking", "booking__user")
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        if not getattr(self.request, "user", None) or not self.request.user.is_authenticated:
            return BookingPayment.objects.none()
        return self.queryset.filter(booking__user=self.request.user)

    def get_serializer_class(self):
        if self.action in {"create", "partial_update"}:
            return BookingPaymentWriteSerializer
        return BookingPaymentSerializer

    def perform_create(self, serializer):
        booking = get_object_or_404(Booking, pk=self.request.data.get("booking"), user=self.request.user)
        serializer.save(booking=booking)
