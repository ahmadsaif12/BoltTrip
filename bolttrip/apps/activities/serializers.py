from decimal import Decimal
from rest_framework import serializers
from .models import Activity, ActivityCategory


class ActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "icon_url",
            "is_featured",
        ]


class ActivitySerializer(serializers.ModelSerializer):
    category = ActivityCategorySerializer(read_only=True)

    class Meta:
        model = Activity
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "category",
            "destination",
            "country",
            "location_text",
            "duration_hours",
            "duration_days",
            "min_group_size",
            "max_group_size",
            "min_age",
            "base_price",
            "discounted_price",
            "currency",
            "rating",
            "review_count",
            "cover_image_url",
            "gallery_image_urls",
            "highlights",
            "includes",
            "excludes",
            "is_featured",
            "created_at",
            "updated_at",
        ]


class ActivityWriteSerializer(serializers.ModelSerializer):
    duration_hours = serializers.IntegerField(min_value=1)
    duration_days = serializers.IntegerField(min_value=1)
    min_group_size = serializers.IntegerField(min_value=1)
    max_group_size = serializers.IntegerField(min_value=1)
    min_age = serializers.IntegerField(min_value=0, max_value=120, required=False, allow_null=True)
    review_count = serializers.IntegerField(min_value=0, required=False)
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0.00"))
    discounted_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0.00"), required=False, allow_null=True)
    currency = serializers.CharField(min_length=3, max_length=3, required=False)

    class Meta:
        model = Activity
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "category",
            "destination",
            "country",
            "location_text",
            "duration_hours",
            "duration_days",
            "min_group_size",
            "max_group_size",
            "min_age",
            "base_price",
            "discounted_price",
            "currency",
            "rating",
            "review_count",
            "cover_image_url",
            "gallery_image_urls",
            "highlights",
            "includes",
            "excludes",
            "is_featured",
            "is_active",
            "sort_order",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if "currency" in attrs and attrs["currency"]:
            attrs["currency"] = attrs["currency"].upper()
        min_group_size = attrs.get("min_group_size", getattr(self.instance, "min_group_size", None))
        max_group_size = attrs.get("max_group_size", getattr(self.instance, "max_group_size", None))
        if min_group_size and max_group_size and max_group_size < min_group_size:
            raise serializers.ValidationError({"max_group_size": "Max group size cannot be smaller than min group size."})
        base_price = attrs.get("base_price", getattr(self.instance, "base_price", None))
        discounted_price = attrs.get("discounted_price", getattr(self.instance, "discounted_price", None))
        if discounted_price is not None and base_price is not None and discounted_price > base_price:
            raise serializers.ValidationError({"discounted_price": "Discounted price cannot be greater than base price."})
        return attrs