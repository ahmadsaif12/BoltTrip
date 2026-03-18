from decimal import Decimal
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.misc.models import BaseModel


class ActivityCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    icon_url = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Activity categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:120]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Activity(BaseModel):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    category = models.ForeignKey(
        ActivityCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activities",
    )

    destination = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    location_text = models.CharField(max_length=180, blank=True, null=True)

    duration_hours = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])
    duration_days = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(0)])
    min_group_size = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])
    max_group_size = models.PositiveSmallIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(500)])
    min_age = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(110)])

    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    currency = models.CharField(max_length=10, default="USD")

    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('5.0'))])
    review_count = models.PositiveIntegerField(default=0)

    cover_image_url = models.URLField()
    gallery_image_urls = models.JSONField(default=list, blank=True)
    highlights = models.JSONField(default=list, blank=True)
    includes = models.JSONField(default=list, blank=True)
    excludes = models.JSONField(default=list, blank=True)

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
