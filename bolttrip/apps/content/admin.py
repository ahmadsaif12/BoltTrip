from django.contrib import admin
from .models import (
    ContentCategory,
    FAQ,
    NewsletterBlock,
    PromoBanner,
    Story,
    Testimonial,
)


@admin.register(ContentCategory)
class ContentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name", "slug")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "destination",
        "published_at",
        "is_featured",
        "is_active",
    )
    search_fields = ("title", "destination", "country", "slug")
    list_filter = ("is_featured", "is_active", "category")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "rating", "is_featured", "is_active")
    search_fields = ("name", "role", "location")
    list_filter = ("is_featured", "is_active")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "page", "is_active", "sort_order")
    search_fields = ("question", "page")
    list_filter = ("is_active", "page")


@admin.register(PromoBanner)
class PromoBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "page", "is_active", "sort_order")
    search_fields = ("title", "page")
    list_filter = ("is_active", "page")


@admin.register(NewsletterBlock)
class NewsletterBlockAdmin(admin.ModelAdmin):
    list_display = ("title", "page", "is_active")
    search_fields = ("title", "page")
    list_filter = ("is_active", "page")
