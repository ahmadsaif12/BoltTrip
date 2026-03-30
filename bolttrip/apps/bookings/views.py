import uuid

from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.misc.schema import (
    booking_payment_viewset_schema,
    booking_traveler_viewset_schema,
    booking_viewset_schema,
)

from .models import Booking, BookingPayment, BookingTraveler, PaymentStatus, PaymentMethod
from .serializers import (
    BookingPaymentSerializer,
    BookingPaymentWriteSerializer,
    BookingSerializer,
    BookingTravelerSerializer,
    BookingTravelerWriteSerializer,
    BookingWriteSerializer,
)
from .payment_gateway import PaymentGateway


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

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def initiate_esewa(self, request):
        """
        Initiate eSewa payment
        Required: booking_id, amount
        """
        try:
            booking_id = request.data.get("booking_id")
            amount = request.data.get("amount")
            
            if not booking_id or not amount:
                return Response(
                    {"error": "booking_id and amount are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            # Verify booking belongs to user
            booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
            
            # Generate payment data
            payment_data = PaymentGateway.initiate_esewa_payment(
                booking_id=booking_id,
                amount=amount,
                product_name=f"Booking {booking.booking_reference}",
            )
            
            return Response(payment_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def initiate_khalti(self, request):
        """
        Initiate Khalti payment
        Required: booking_id, amount
        """
        try:
            booking_id = request.data.get("booking_id")
            amount = request.data.get("amount")
            
            if not booking_id or not amount:
                return Response(
                    {"error": "booking_id and amount are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            # Verify booking belongs to user
            booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
            
            # Generate payment data
            payment_data = PaymentGateway.initiate_khalti_payment(
                booking_id=booking_id,
                amount=amount,
                product_name=f"Booking {booking.booking_reference}",
            )
            
            return Response(payment_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def verify_esewa(self, request):
        """
        Verify eSewa payment
        Required: booking_id, transaction_uuid
        """
        try:
            booking_id = request.data.get("booking_id")
            transaction_uuid = request.data.get("transaction_uuid")
            
            if not booking_id or not transaction_uuid:
                return Response(
                    {"error": "booking_id and transaction_uuid are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            # Verify booking belongs to user
            booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
            
            # Verify payment with eSewa
            verification = PaymentGateway.verify_esewa_payment(transaction_uuid)
            
            if not verification:
                return Response(
                    {"error": "Payment verification failed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if verification.get("success"):
                # Create payment record
                payment = BookingPayment.objects.create(
                    booking=booking,
                    payment_method=PaymentMethod.ESEWA,
                    amount=booking.total_amount,
                    transaction_id=verification.get("transaction_id"),
                    payment_status=PaymentStatus.PAID,
                    currency=booking.currency,
                )
                
                # Update booking payment status
                booking.payment_status = PaymentStatus.PAID
                booking.save()
                
                return Response(
                    {
                        "success": True,
                        "message": "Payment verified successfully",
                        "payment": BookingPaymentSerializer(payment).data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Payment verification failed", "details": verification},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def verify_khalti(self, request):
        """
        Verify Khalti payment
        Required: booking_id, token, amount
        """
        try:
            booking_id = request.data.get("booking_id")
            token = request.data.get("token")
            amount = request.data.get("amount")
            
            if not booking_id or not token or not amount:
                return Response(
                    {"error": "booking_id, token, and amount are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            # Verify booking belongs to user
            booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
            
            # Verify payment with Khalti
            verification = PaymentGateway.verify_khalti_payment(token, amount)
            
            if not verification:
                return Response(
                    {"error": "Payment verification failed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if verification.get("success"):
                # Create payment record
                payment = BookingPayment.objects.create(
                    booking=booking,
                    payment_method=PaymentMethod.KHALTI,
                    amount=booking.total_amount,
                    transaction_id=verification.get("transaction_id"),
                    payment_status=PaymentStatus.PAID,
                    currency=booking.currency,
                )
                
                # Update booking payment status
                booking.payment_status = PaymentStatus.PAID
                booking.save()
                
                return Response(
                    {
                        "success": True,
                        "message": "Payment verified successfully",
                        "payment": BookingPaymentSerializer(payment).data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Payment verification failed", "details": verification},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
