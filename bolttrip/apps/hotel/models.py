from decimal import Decimal
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.misc.models import BaseModel

class Amenity(BaseModel):
    name = models.CharField(max_length=100,unique=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    icon_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Hotel(BaseModel):
    PROPERTY_TYPE_CHOICES = [
        ("hotel", "Hotel"),
        ("resort", "Resort"),
        ("villa", "Villa"),
        ("apartment", "Apartment"),
        ("lodge", "Lodge"),
        ("hostel", "Hostel"),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default="hotel")
    star_rating = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('5.0'))])
    review_count = models.PositiveIntegerField(default=0)

    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    currency = models.CharField(max_length=10, default="USD")

    is_deal = models.BooleanField(default=False)
    deal_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    deal_end_at = models.DateTimeField(blank=True, null=True)
    main_image_url = models.URLField(blank=True, null=True)
    gallery_image_urls = models.JSONField(default=list, blank=True)

    check_in_time = models.TimeField(blank=True, null=True)
    check_out_time = models.TimeField(blank=True, null=True)

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    amenities = models.ManyToManyField(Amenity, blank=True, related_name="hotels")

    def save(self , *args , **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:220]
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class RoomType(BaseModel):
    Bed_Type_Choices= [
        ("single","Single"),
        ("double","Double"),
        ("queen","Queen"),
        ("king","King"),
        ("twin", "Twin"),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    name = models.CharField(max_length=100)
    bed_type = models.CharField(max_length=20, choices=Bed_Type_Choices, default="double")
    capacity = models.PositiveSmallIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(20)])
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0)])

    room_image_urls = models.JSONField(default=list,blank=True)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="room_types")

    def __str__(self):
        return f"{self.hotel.name}- {self.name}"
    
