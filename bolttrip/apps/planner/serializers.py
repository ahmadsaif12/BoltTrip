from decimal import Decimal
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
    travelers_count = serializers.IntegerField(min_value=1, max_value=50)
    estimated_budget = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.00"),
        required=False,
        allow_null=True,
    )
    currency = serializers.CharField(min_length=3, max_length=3, required=False)

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

    def validate(self, attrs):
        attrs = super().validate(attrs)
        # normalize currency
        if "currency" in attrs and attrs["currency"]:
            attrs["currency"] = attrs["currency"].upper()

        # validate start/end dates
        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "End date cannot be earlier than start date."})
        return attrs


class PlannerFaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannerFaq
        fields = [
            "id",
            "question",
            "answer",
        ]