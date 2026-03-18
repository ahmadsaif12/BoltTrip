from rest_framework import serializers
from .models import (
    ItineraryTemplate,
    PlannerFaq,
    SmartSuggestion,
    TravelPlan,
    TravelPlanDay,
    TravelPlanItem,
)


class ItineraryTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryTemplate
        fields = [
            "id",
            "title",
            "slug",
            "destination",
            "country",
            "short_description",
            "description",
            "start_date",
            "duration_days",
            "traveler_capacity",
            "base_price",
            "currency",
            "rating",
            "hero_image_url",
            "gallery_image_urls",
            "highlights",
            "is_featured",
            "created_at",
            "updated_at",
        ]


class SmartSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartSuggestion
        fields = [
            "id",
            "title",
            "suggestion_type",
            "description",
            "icon_name",
        ]


class TravelPlanItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPlanItem
        fields = [
            "id",
            "item_type",
            "title",
            "description",
            "start_time",
            "end_time",
            "location",
            "sort_order",
        ]


class TravelPlanDaySerializer(serializers.ModelSerializer):
    items = TravelPlanItemSerializer(many=True, read_only=True)

    class Meta:
        model = TravelPlanDay
        fields = [
            "id",
            "day_number",
            "title",
            "description",
            "items",
        ]


class TravelPlanSerializer(serializers.ModelSerializer):
    days = TravelPlanDaySerializer(many=True, read_only=True)
    based_on_template = ItineraryTemplateSerializer(read_only=True)

    class Meta:
        model = TravelPlan
        fields = [
            "id",
            "title",
            "destination",
            "country",
            "start_date",
            "end_date",
            "travelers_count",
            "estimated_budget",
            "currency",
            "status",
            "based_on_template",
            "notes",
            "days",
            "created_at",
            "updated_at",
        ]


class TravelPlanWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPlan
        fields = [
            "id",
            "title",
            "destination",
            "country",
            "start_date",
            "end_date",
            "travelers_count",
            "estimated_budget",
            "currency",
            "status",
            "based_on_template",
            "notes",
        ]
        read_only_fields = ["id"]


class PlannerFaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannerFaq
        fields = [
            "id",
            "question",
            "answer",
        ]
