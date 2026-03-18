from decimal import Decimal
from rest_framework import serializers
from apps.activities.models import Activity
from apps.hotel.models import Hotel
from apps.packages.models import TravelPackage
from apps.users.models import GuideProfile
from .models import (
    Booking,
    BookingPayment,
    BookingStatus,
    BookingTraveler,
    BookingType,
    PaymentMethod,
    PaymentStatus,
    TravelerGender,
)


def validate_traveler_age(value):
    """Validate traveler age is within realistic bounds."""
    if value is not None and value > 110:
        raise serializers.ValidationError(
            "Age must be 110 or less. Please ensure the age is accurate."
        )
    return value


class BookingTravelerSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(
        required=False,
        allow_null=True,
        validators=[validate_traveler_age]
    )

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
    user = serializers.UUIDField(source="user_id", read_only=True)
    package = serializers.IntegerField(source="package_id", read_only=True, allow_null=True)
    hotel = serializers.IntegerField(source="hotel_id", read_only=True, allow_null=True)
    activity = serializers.IntegerField(source="activity_id", read_only=True, allow_null=True)
    guide = serializers.IntegerField(source="guide_id", read_only=True, allow_null=True)
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
    booking_type = serializers.ChoiceField(choices=BookingType.choices)
    booking_status = serializers.ChoiceField(choices=BookingStatus.choices, required=False)
    payment_status = serializers.ChoiceField(choices=PaymentStatus.choices, required=False)
    package = serializers.PrimaryKeyRelatedField(queryset=TravelPackage.objects.filter(is_active=True), required=False, allow_null=True)
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.filter(is_active=True), required=False, allow_null=True)
    activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.filter(is_active=True), required=False, allow_null=True)
    guide = serializers.PrimaryKeyRelatedField(queryset=GuideProfile.objects.filter(is_available=True), required=False, allow_null=True)
    travelers_count = serializers.IntegerField(min_value=1, max_value=50)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0.00"))
    paid_amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0.00"), required=False)
    currency = serializers.CharField(min_length=3, max_length=3)
    contact_name = serializers.CharField(max_length=120)
    contact_email = serializers.EmailField()
    contact_phone = serializers.CharField(max_length=30, required=False, allow_blank=True, allow_null=True)
    special_requests = serializers.CharField(required=False, allow_blank=True, allow_null=True)

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

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if "currency" in attrs and attrs["currency"]:
            attrs["currency"] = attrs["currency"].upper()
        booking_type = attrs.get("booking_type", getattr(self.instance, "booking_type", None))
        selected_targets = {
            BookingType.PACKAGE: attrs.get("package", getattr(self.instance, "package", None)),
            BookingType.HOTEL: attrs.get("hotel", getattr(self.instance, "hotel", None)),
            BookingType.ACTIVITY: attrs.get("activity", getattr(self.instance, "activity", None)),
            BookingType.GUIDE: attrs.get("guide", getattr(self.instance, "guide", None)),
        }
        populated_targets = [key for key, value in selected_targets.items() if value is not None]
        if len(populated_targets) != 1:
            raise serializers.ValidationError("Select exactly one of package, hotel, activity, or guide.")
        if booking_type not in populated_targets:
            raise serializers.ValidationError({"booking_type": "Booking type must match the selected target."})
        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "End date cannot be earlier than start date."})
        total_amount = attrs.get("total_amount", getattr(self.instance, "total_amount", None))
        paid_amount = attrs.get("paid_amount", getattr(self.instance, "paid_amount", None))
        if total_amount is not None and paid_amount is not None and paid_amount > total_amount:
            raise serializers.ValidationError({"paid_amount": "Paid amount cannot be greater than total amount."})
        return attrs


class BookingTravelerWriteSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(min_value=0, max_value=120, required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=TravelerGender.choices, required=False, allow_null=True)

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

    def validate_age(self, value):
        if value is not None and value > 120:
            raise serializers.ValidationError("Age must be 120 or below.")
        return value


class BookingPaymentWriteSerializer(serializers.ModelSerializer):
    payment_method = serializers.ChoiceField(choices=PaymentMethod.choices)
    payment_status = serializers.ChoiceField(choices=PaymentStatus.choices, required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0.01"))
    currency = serializers.CharField(min_length=3, max_length=3)

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

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_currency(self, value):
        return value.upper()