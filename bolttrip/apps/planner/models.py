from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.misc.models import BaseModel


class TravelPlanStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    READY = "ready", "Ready"
    BOOKED = "booked", "Booked"


class ItineraryTemplate(BaseModel):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    destination = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    short_description = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    duration_days = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(365)])
    traveler_capacity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(500)])
    base_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    currency = models.CharField(max_length=10, default="USD")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('5.0'))])
    hero_image_url = models.URLField()
    gallery_image_urls = models.JSONField(default=list, blank=True)
    highlights = models.JSONField(default=list, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:200]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class SmartSuggestion(BaseModel):
    SUGGESTION_TYPE_CHOICES = [
        ("event", "Nearby Event"),
        ("restaurant", "Restaurant"),
        ("emergency", "Emergency Contact"),
        ("weather", "Weather Update"),
        ("tip", "Travel Tip"),
    ]

    title = models.CharField(max_length=150)
    suggestion_type = models.CharField(max_length=20, choices=SUGGESTION_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    icon_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class TravelPlan(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="travel_plans",
    )
    title = models.CharField(max_length=180)
    destination = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    travelers_count = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(500)])
    estimated_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    currency = models.CharField(max_length=10, default="USD")
    status = models.CharField(
        max_length=20,
        choices=TravelPlanStatus.choices,
        default=TravelPlanStatus.DRAFT,
    )
    based_on_template = models.ForeignKey(
        ItineraryTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_plans",
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class TravelPlanDay(BaseModel):
    plan = models.ForeignKey(
        TravelPlan,
        on_delete=models.CASCADE,
        related_name="days",
    )
    day_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(365)])
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["day_number"]
        unique_together = ("plan", "day_number")

    def __str__(self):
        return f"{self.plan.title} - Day {self.day_number}"


class TravelPlanItem(BaseModel):
    ITEM_TYPE_CHOICES = [
        ("flight", "Flight"),
        ("hotel", "Hotel Check-In"),
        ("activity", "Activity"),
        ("meal", "Meal"),
        ("transfer", "Transfer"),
        ("note", "Note"),
    ]

    day = models.ForeignKey(
        TravelPlanDay,
        on_delete=models.CASCADE,
        related_name="items",
    )
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=180, blank=True, null=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "start_time", "id"]

    def __str__(self):
        return self.title


class PlannerFaq(BaseModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.question
