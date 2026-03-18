from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.misc.models import BaseModel


class BookingType(models.TextChoices):
    PACKAGE = "package", "Package"
    HOTEL = "hotel", "Hotel"
    ACTIVITY = "activity", "Activity"
    GUIDE = "guide", "Guide"


class BookingStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"
    COMPLETED = "completed", "Completed"


class PaymentStatus(models.TextChoices):
    UNPAID = "unpaid", "Unpaid"
    PAID = "paid", "Paid"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"


class PaymentMethod(models.TextChoices):
    CARD = "card", "Card"
    BANK_TRANSFER = "bank_transfer", "Bank Transfer"
    WALLET = "wallet", "Wallet"
    CASH = "cash", "Cash"
    OTHER = "other", "Other"


class TravelerGender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"


class Booking(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    booking_type = models.CharField(max_length=20, choices=BookingType.choices)
    booking_status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.UNPAID,
    )

    package = models.ForeignKey(
        "packages.TravelPackage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )
    hotel = models.ForeignKey(
        "hotel.Hotel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )
    activity = models.ForeignKey(
        "activities.Activity",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )
    guide = models.ForeignKey(
        "users.GuideProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )

    booking_reference = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    travelers_count = models.PositiveSmallIntegerField(default=1)

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    currency = models.CharField(max_length=3, default="USD")

    contact_name = models.CharField(max_length=120)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=30, blank=True, null=True)
    special_requests = models.TextField(blank=True, null=True)

    confirmed_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        selected_targets = {
            BookingType.PACKAGE: self.package_id,
            BookingType.HOTEL: self.hotel_id,
            BookingType.ACTIVITY: self.activity_id,
            BookingType.GUIDE: self.guide_id,
        }
        populated_targets = [key for key, value in selected_targets.items() if value]

        if len(populated_targets) != 1:
            raise ValidationError("A booking must reference exactly one bookable item.")

        if self.booking_type not in populated_targets:
            raise ValidationError(
                {"booking_type": "Booking type must match the selected package, hotel, activity, or guide."}
            )

        if self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "End date cannot be earlier than start date."})

        if self.paid_amount > self.total_amount:
            raise ValidationError({"paid_amount": "Paid amount cannot be greater than total amount."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.booking_reference


class BookingTraveler(BaseModel):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="travelers",
    )
    full_name = models.CharField(max_length=120)
    age = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(110)],
    )
    gender = models.CharField(
        max_length=20,
        choices=TravelerGender.choices,
        blank=True,
        null=True,
    )
    nationality = models.CharField(max_length=80, blank=True, null=True)
    passport_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.full_name


class BookingPayment(BaseModel):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    currency = models.CharField(max_length=3, default="USD")
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.UNPAID,
    )
    paid_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.amount <= 0:
            raise ValidationError({"amount": "Payment amount must be greater than zero."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking.booking_reference} - {self.amount}"
