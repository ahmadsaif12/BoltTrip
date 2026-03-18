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
