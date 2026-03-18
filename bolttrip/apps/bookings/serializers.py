from rest_framework import serializers

from .models import Booking, BookingPayment, BookingTraveler


class BookingTravelerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingTraveler
        fields = [
            "id",
            "full_name",
            "age",
            "gender",
            "nationality",
            "passport_number",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class BookingPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPayment
        fields = [
            "id",
            "transaction_id",
            "payment_method",
            "amount",
            "currency",
            "payment_status",
            "paid_at",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class BookingSerializer(serializers.ModelSerializer):
    travelers = BookingTravelerSerializer(many=True, read_only=True)
    payments = BookingPaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "booking_type",
            "booking_status",
            "payment_status",
            "package",
            "hotel",
            "activity",
            "guide",
            "booking_reference",
            "start_date",
            "end_date",
            "travelers_count",
            "total_amount",
            "paid_amount",
            "currency",
            "contact_name",
            "contact_email",
            "contact_phone",
            "special_requests",
            "confirmed_at",
            "cancelled_at",
            "travelers",
            "payments",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "booking_reference",
            "created_at",
            "updated_at",
        ]


class BookingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "booking_type",
            "booking_status",
            "payment_status",
            "package",
            "hotel",
            "activity",
            "guide",
            "start_date",
            "end_date",
            "travelers_count",
            "total_amount",
            "paid_amount",
            "currency",
            "contact_name",
            "contact_email",
            "contact_phone",
            "special_requests",
            "confirmed_at",
            "cancelled_at",
        ]
        read_only_fields = ["id"]


class BookingTravelerWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingTraveler
        fields = [
            "id",
            "booking",
            "full_name",
            "age",
            "gender",
            "nationality",
            "passport_number",
        ]
        read_only_fields = ["id"]


class BookingPaymentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPayment
        fields = [
            "id",
            "booking",
            "transaction_id",
            "payment_method",
            "amount",
            "currency",
            "payment_status",
            "paid_at",
            "notes",
        ]
        read_only_fields = ["id"]
