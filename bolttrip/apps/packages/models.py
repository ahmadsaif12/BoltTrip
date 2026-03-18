from django.db import models
from django.utils.text import slugify
from apps.misc.models import BaseModel
# Create your models here.

class PackageCategory(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    icon_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
     
    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = slugify(self.name)
      super().save(*args, **kwargs)

    def __str__(self):
       return self.name
    
class Destination(BaseModel):
    name = models.CharField(max_length=130)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    country = models.CharField(max_length=100)
    hero_image_url = models.URLField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'country')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.country}")[:140]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.country}"


class TravelPackage(BaseModel):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    category = models.ForeignKey(
        PackageCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="packages",
    )
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="packages",
    )

    duration_days = models.PositiveSmallIntegerField(default=1)
    duration_nights = models.PositiveSmallIntegerField(default=0)
    location_text = models.CharField(max_length=180)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    review_count = models.PositiveIntegerField(default=0)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10, default="USD")
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