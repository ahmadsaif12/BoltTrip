import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.misc.models import BaseModel

from .manager import CustomUserManager


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserType(models.TextChoices):
    TRAVELER = "traveler", "Traveler"
    COMPANY = "company", "Travel Company"
    HOTEL_OWNER = "hotel_owner", "Hotel Owner"
    ADMIN = "admin", "Admin"
    GUIDE = "guide", "Guide"
    MANAGER = "manager", "Manager"
    SEO = "seo", "SEO Team"
    CONTENT = "content", "Content Writer"
    SUPPORT = "support", "Support Agent"


class MaritalStatus(models.TextChoices):
    MARRIED = "married", "Married"
    UNMARRIED = "unmarried", "Unmarried"


class ProfileType(models.TextChoices):
    GUEST = "guest", "Guest"
    BASIC = "basic", "Basic"
    VERIFIED = "verified", "Verified"


class KycStatus(models.TextChoices):
    APPROVED = "approved", "Approved"
    PENDING = "pending", "Pending"
    REJECTED = "rejected", "Rejected"


class PaymentType(models.TextChoices):
    FONEPAY = "fonepay", "Fonepay"
    CARD = "card", "Card"
    WALLET = "wallet", "Wallet"
    CASH = "cash", "Cash"


class PriceSensitivity(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"


class Gender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"


class ThemeChoice(models.TextChoices):
    LIGHT = "light", "Light"
    DARK = "dark", "Dark"


class GuideType(models.TextChoices):
    CITY = "city", "City Guide"
    HIKING = "hiking", "Hiking Guide"
    TREKKING = "trekking", "Trekking Guide"


class GuideProfileStatus(models.TextChoices):
    PENDING_AFFILIATION = "pending_affiliation", "Pending Affiliation"
    AFFILIATED_PENDING_APPROVAL = "affiliated_pending_approval", "Affiliated Pending Approval"
    APPROVED = "approved", "Approved & Active"
    REJECTED = "rejected", "Rejected"
    SUSPENDED = "suspended", "Suspended"


class NotificationType(models.TextChoices):
    DEAL = "deal", "Deal"
    FLIGHT = "flight", "Flight Change"
    SAFETY = "safety", "Safety Update"


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.TRAVELER,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email


class UserOTP(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="otp_codes",
    )
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - OTP"


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=MaritalStatus.choices,
        default=MaritalStatus.UNMARRIED,
    )
    dob = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    preferred_pronouns = models.CharField(max_length=50, blank=True, null=True)
    theme = models.CharField(max_length=10, choices=ThemeChoice.choices, default=ThemeChoice.LIGHT)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    preferred_currency = models.CharField(max_length=10, blank=True, null=True)
    preferred_timezone = models.CharField(max_length=50, blank=True, null=True)
    passport_country = models.CharField(max_length=100, blank=True, null=True)
    profile_type = models.CharField(
        max_length=20,
        choices=ProfileType.choices,
        default=ProfileType.GUEST,
    )
    id_card_number = models.CharField(max_length=20, blank=True, null=True)
    kyc_status = models.CharField(
        max_length=20,
        choices=KycStatus.choices,
        default=KycStatus.PENDING,
    )
    emergency_contact = models.CharField(max_length=30, blank=True, null=True)
    medical_conditions = models.TextField(blank=True, null=True)
    preferred_payment_type = models.CharField(
        max_length=20,
        choices=PaymentType.choices,
        default=PaymentType.FONEPAY,
    )
    budget_range = models.CharField(max_length=50, blank=True, null=True)
    price_sensitivity_level = models.CharField(
        max_length=10,
        choices=PriceSensitivity.choices,
        default=PriceSensitivity.MEDIUM,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.name}'s Profile"


class GuideProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guide_profile",
    )
    travel_company = models.CharField(max_length=255, blank=True, null=True)
    profile_photo = models.URLField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    dob = models.DateField()
    nationality = models.CharField(max_length=100)
    guide_type = models.CharField(max_length=20, choices=GuideType.choices)
    status = models.CharField(
        max_length=50,
        choices=GuideProfileStatus.choices,
        default=GuideProfileStatus.PENDING_AFFILIATION,
    )
    languages_spoken = models.JSONField(default=list, blank=True)
    specializations = models.JSONField(default=list, blank=True)
    region_expertise = models.JSONField(default=list, blank=True)
    guide_license_number = models.CharField(max_length=100)
    license_document = models.URLField(blank=True, null=True)
    license_expiry = models.DateField()
    tourism_board_id = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    years_of_experience = models.PositiveIntegerField()
    certifications = models.JSONField(default=list, blank=True)
    languages_certified = models.JSONField(default=list, blank=True)
    previous_companies = models.TextField(blank=True, null=True)
    total_groups_led = models.PositiveIntegerField(default=0)
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    custom_rates = models.JSONField(default=list, blank=True)
    unavailable_dates = models.JSONField(default=list, blank=True)
    accepts_group_bookings = models.BooleanField(default=True)
    max_group_size = models.PositiveIntegerField(default=10)
    accepts_last_minute = models.BooleanField(default=True)
    last_minute_buffer_days = models.PositiveIntegerField(default=2)
    linked_packages = models.JSONField(default=list, blank=True)
    base_city = models.CharField(max_length=100)
    base_country = models.CharField(max_length=100)
    available_regions = models.JSONField(default=list, blank=True)
    willing_to_travel = models.BooleanField(default=True)
    max_travel_distance_km = models.PositiveIntegerField(default=100)
    gallery_images = models.JSONField(default=list, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    review_tags = models.JSONField(default=list, blank=True)
    notify_booking = models.BooleanField(default=True)
    notify_reviews = models.BooleanField(default=True)
    notify_cancellations = models.BooleanField(default=True)
    enable_in_app_chat = models.BooleanField(default=False)
    id_proof = models.URLField(blank=True, null=True)
    address_proof = models.URLField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=100)
    police_clearance = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    admin_notes = models.TextField(blank=True, null=True)
    force_availability_override = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Guide: {self.user.name} ({self.user.email})"


class Wishlist(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlists",
    )
    destination_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    package = models.CharField(max_length=255, blank=True, null=True)
    hotel = models.ForeignKey(
        "hotel.Hotel",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="wishlist_hotels",
    )
    guide = models.ForeignKey(
        "users.GuideProfile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="wishlist_guides",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.name} - {self.destination_name}"


class Notification(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    message = models.TextField()
    notification_type = models.CharField(
        max_length=50,
        choices=NotificationType.choices,
        verbose_name="Notification Type",
    )
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.name} - {self.message[:20]}"
