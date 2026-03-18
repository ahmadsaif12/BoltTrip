from django.contrib import admin
from .models import TourPackage, TourType


@admin.register(TourType)
class TourTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "destination",
        "country",
        "package_type",
        "base_price",
        "discounted_price",
        "is_featured",
        "is_active",
    )
    search_fields = ("title", "destination", "country", "slug")
    list_filter = ("is_featured", "is_active", "package_type", "country")
    prepopulated_fields = {"slug": ("title",)}
