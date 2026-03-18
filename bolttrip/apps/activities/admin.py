from django.contrib import admin
from .models import Activity, ActivityCategory


@admin.register(ActivityCategory)
class ActivityCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_featured", "is_active", "created_at")
    search_fields = ("name", "slug")
    list_filter = ("is_featured", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "destination",
        "country",
        "category",
        "base_price",
        "discounted_price",
        "is_featured",
        "is_active",
    )
    search_fields = ("title", "destination", "country", "slug")
    list_filter = ("is_featured", "is_active", "category", "country")
    prepopulated_fields = {"slug": ("title",)}
