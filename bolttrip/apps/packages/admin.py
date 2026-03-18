from django.contrib import admin
from .models import Destination, PackageCategory, TravelPackage


@admin.register(PackageCategory)
class PackageCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "is_featured", "is_active")
    search_fields = ("name", "country")
    list_filter = ("is_featured", "is_active", "country")
    prepopulated_fields = {"slug": ("name", "country")}


@admin.register(TravelPackage)
class TravelPackageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "destination",
        "category",
        "duration_days",
        "base_price",
        "discounted_price",
        "is_featured",
        "is_active",
    )
    search_fields = ("title", "destination__name", "destination__country", "slug")
    list_filter = ("is_featured", "is_active", "category", "destination__country")
    prepopulated_fields = {"slug": ("title",)}
