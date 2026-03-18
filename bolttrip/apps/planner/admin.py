from django.contrib import admin
from .models import (
    ItineraryTemplate,
    PlannerFaq,
    SmartSuggestion,
    TravelPlan,
    TravelPlanDay,
    TravelPlanItem,
)


class TravelPlanItemInline(admin.TabularInline):
    model = TravelPlanItem
    extra = 0


class TravelPlanDayInline(admin.StackedInline):
    model = TravelPlanDay
    extra = 0


@admin.register(ItineraryTemplate)
class ItineraryTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "destination",
        "country",
        "start_date",
        "base_price",
        "is_featured",
        "is_active",
    )
    search_fields = ("title", "destination", "country", "slug")
    list_filter = ("is_featured", "is_active", "country")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(SmartSuggestion)
class SmartSuggestionAdmin(admin.ModelAdmin):
    list_display = ("title", "suggestion_type", "is_active")
    search_fields = ("title",)
    list_filter = ("suggestion_type", "is_active")


@admin.register(TravelPlan)
class TravelPlanAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "destination", "start_date", "status", "created_at")
    search_fields = ("title", "destination", "country", "user__email")
    list_filter = ("status", "country")
    inlines = [TravelPlanDayInline]


@admin.register(TravelPlanDay)
class TravelPlanDayAdmin(admin.ModelAdmin):
    list_display = ("plan", "day_number", "title")
    search_fields = ("plan__title", "title")
    inlines = [TravelPlanItemInline]


@admin.register(PlannerFaq)
class PlannerFaqAdmin(admin.ModelAdmin):
    list_display = ("question", "is_active", "sort_order")
    search_fields = ("question",)
    list_filter = ("is_active",)
