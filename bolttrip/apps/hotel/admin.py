from django.contrib import admin
from .models import Hotel, RoomType, Amenity

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country", "property_type", "rating", "price_per_night", "is_active")
    list_filter = ("property_type", "city", "country", "is_active", "is_featured")
    search_fields = ("name", "city", "country")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ("hotel", "name", "bed_type", "capacity", "price_per_night", "quantity")
    list_filter = ("bed_type",)

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name", "category")