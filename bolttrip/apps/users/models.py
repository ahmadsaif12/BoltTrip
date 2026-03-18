import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .manager import CustomUserManager
from apps.misc.models import BaseModel

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    User_Type_Choices= [
        ("traveler","Traveler"),
        ("company","Travel Company"),
        ("hotel_owner","Hotel Owner"),
        ("admin","Admin"),
        ("guide","Guide"),
        ("manager","Manager"),
        ("seo","SEO Team"),
        ("content","Content Writer"),
        ("support","Support Agent")
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20,blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=User_Type_Choices, default="traveler")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class UserOTP(TimeStampedModel):
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name= "otp")
        otp = models.CharField(max_length= 6)
        is_verified = models.BooleanField(default= False)

        class Meta:
            ordering = ["-created_at"]

        def __str__(self):
            return f"{self.user.email} - OTP"
        
class UserProfile(TimeStampedModel):
     status_choices= [("married","Married"),("unmarried","Unmarried")]
     Profile_Type_Choices= [("guest","Guest"),("basic","Basic"),("verified","Verified")]
     Kyc_Status_Choices= [("approved","Approved"),("pending","Pending"),("rejected","Rejected")]
     Payment_Type_Choices = [("fonepay","Fonepay"),("card","Card"),("wallet","Wallet"),("cash","Cash")]
     Price_Sensitivity_Choices= [("low","Low"),("medium","Medium"),("high","High")]
     Gender_Choices= [("male","Male"),("female","Female"),("other","Other")]
     THEME_CHOICES = [("light", "Light"), ("dark", "Dark")]
     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
     address = models.CharField(max_length=255, blank=True, null= True)
     gender = models.CharField(max_length=20 , choices=Gender_Choices, blank=True ,null=True)
     status = models.CharField(max_length=20, choices=status_choices, default="unmarried")
     dob = models.DateField(blank=True, null=True)
     bio = models.TextField(blank=True, null=True)
     nationality = models.CharField(max_length=50, blank=True, null=True)
     profile_picture = models.URLField(blank=True, null=True)
     preferred_pronouns = models.CharField(max_length=50, blank=True, null=True)
     theme = models.CharField(max_length=10, choices=THEME_CHOICES, default="light")
     city = models.CharField(max_length=100, blank=True, null=True)
     country = models.CharField(max_length=100, blank=True, null=True)
     preferred_currency = models.CharField(max_length=10, blank=True, null=True)
     preferred_timezone = models.CharField(max_length=50, blank=True, null=True)
     passport_country = models.CharField(max_length=100, blank=True, null=True)
     profile_type = models.CharField(max_length=20, choices=Profile_Type_Choices, default="guest")
     id_card_number = models.CharField(max_length=20, blank=True, null=True)
     kyc_status = models.CharField(max_length=20, choices=Kyc_Status_Choices, default="pending")
     emergency_contact = models.CharField(max_length=30, blank=True, null=True)
     medical_conditions = models.TextField(blank=True, null=True)
     preferred_payment_type = models.CharField(max_length=20, choices=Payment_Type_Choices, default="fonepay")
     budget_range = models.CharField(max_length=50, blank=True, null=True)
     price_sensitivity_level = models.CharField(max_length=10, choices=Price_Sensitivity_Choices, default="medium")

     def __str__(self):
        return f"{self.user.name}'s Profile"

class GuideProfile(models.Model):
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    GUIDE_TYPE_CHOICES = [('city', 'City Guide'), ('hiking', 'Hiking Guide'), ('trekking', 'Trekking Guide')]
    PROFILE_STATUS_CHOICES = [
        ('pending_affiliation', 'Pending Affiliation'),
        ('affiliated_pending_approval', 'Affiliated Pending Approval'),
        ('approved', 'Approved & Active'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guide_profile')
    travel_company = models.CharField(max_length=255, blank=True, null=True)
    profile_photo = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    nationality = models.CharField(max_length=100)
    guide_type = models.CharField(max_length=20, choices=GUIDE_TYPE_CHOICES)
    status = models.CharField(max_length=50, choices=PROFILE_STATUS_CHOICES, default='pending_affiliation')
    languages_spoken = models.CharField(max_length=1000, blank=True, null=True)
    specializations = models.CharField(max_length=1000, blank=True, null=True)
    region_expertise = models.CharField(max_length=1000, blank=True, null=True)
    guide_license_number = models.CharField(max_length=100)
    license_document = models.TextField(null=True, blank=True)
    license_expiry = models.DateField()
    tourism_board_id = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    years_of_experience = models.PositiveIntegerField()
    certifications = models.CharField(max_length=1000, blank=True, null=True)
    languages_certified = models.CharField(max_length=1000, blank=True, null=True)
    previous_companies = models.TextField(blank=True, null=True)
    total_groups_led = models.PositiveIntegerField(default=0)
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    custom_rates = models.CharField(max_length=1000, blank=True, null=True)
    unavailable_dates = models.CharField(max_length=1000, blank=True, null=True)
    accepts_group_bookings = models.BooleanField(default=True)
    max_group_size = models.PositiveIntegerField(default=10)
    accepts_last_minute = models.BooleanField(default=True)
    last_minute_buffer_days = models.PositiveIntegerField(default=2)
    linked_packages = models.JSONField(default=list, blank=True)
    base_city = models.CharField(max_length=100)
    base_country = models.CharField(max_length=100)
    available_regions = models.CharField(max_length=1000, blank=True, null=True)
    willing_to_travel = models.BooleanField(default=True)
    max_travel_distance_km = models.PositiveIntegerField(default=100)
    gallery_images = models.CharField(max_length=1000, blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    review_tags = models.CharField(max_length=1000, blank=True, null=True)
    notify_booking = models.BooleanField(default=True)
    notify_reviews = models.BooleanField(default=True)
    notify_cancellations = models.BooleanField(default=True)
    enable_in_app_chat = models.BooleanField(default=False)
    id_proof = models.TextField(blank=True, null=True)
    address_proof = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=100)
    police_clearance = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    admin_notes = models.TextField(blank=True, null=True)
    force_availability_override = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Guide: {self.user.name} ({self.user.email})"

class Wishlist(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    destination_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    package = models.CharField(max_length=255, null=True, blank=True)
    hotel = models.ForeignKey('hotel.Hotel', on_delete=models.CASCADE, null=True, blank=True, related_name='wishlist_hotels')
    guide = models.ForeignKey('users.GuideProfile', on_delete=models.CASCADE, null=True, blank=True, related_name='wishlist_guides')
    
    def __str__(self):
        return f"{self.user.name} - {self.destination_name}"
    
class Notification(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=50,
        choices=[('deal', 'Deal'), ('flight', 'Flight Change'), ('safety', 'Safety Update')],
        verbose_name="Notification Type"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.name} - {self.message[:20]}"
