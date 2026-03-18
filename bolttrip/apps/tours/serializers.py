from rest_framework import serializers
from .models import  TourType,TourPackage


class TourTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourType
        fields = [
            "id",
            "name",
            "description",
            "icon_url",
        ]

class TourPackageSerializer(serializers.ModelSerializer):
    package_type = TourTypeSerializer(read_only=True)

    class Meta:
        model = TourPackage
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "package_type",
            "destination",
            "country",
            "duration_days",
            "duration_nights",
            "group_size",
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


class TourPackageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPackage
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "package_type",
            "destination",
            "country",
            "duration_days",
            "duration_nights",
            "group_size",
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