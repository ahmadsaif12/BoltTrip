from rest_framework import serializers
from .models import Destination, PackageCategory, TravelPackage


class PackageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageCategory
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "icon_url",
        ]


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = [
            "id",
            "name",
            "slug",
            "country",
            "hero_image_url",
            "summary",
            "is_featured",
        ]


class TravelPackageSerializer(serializers.ModelSerializer):
    category = PackageCategorySerializer(read_only=True)
    destination = DestinationSerializer(read_only=True)

    class Meta:
        model = TravelPackage
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "category",
            "destination",
            "duration_days",
            "duration_nights",
            "location_text",
            "rating",
            "review_count",
            "base_price",
            "discounted_price",
            "currency",
            "cover_image_url",
            "gallery_image_urls",
            "highlights",
            "includes",
            "excludes",
            "is_featured",
            "created_at",
            "updated_at",
        ]


class TravelPackageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPackage
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "category",
            "destination",
            "duration_days",
            "duration_nights",
            "location_text",
            "rating",
            "review_count",
            "base_price",
            "discounted_price",
            "currency",
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
