from decimal import Decimal
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
    duration_days = serializers.IntegerField(min_value=1)
    duration_nights = serializers.IntegerField(min_value=0)
    review_count = serializers.IntegerField(min_value=0, required=False)
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0.00"))
    discounted_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.00"),
        required=False,
        allow_null=True,
    )
    currency = serializers.CharField(min_length=3, max_length=3, required=False)

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

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if "currency" in attrs and attrs["currency"]:
            attrs["currency"] = attrs["currency"].upper()
        base_price = attrs.get("base_price", getattr(self.instance, "base_price", None))
        discounted_price = attrs.get("discounted_price", getattr(self.instance, "discounted_price", None))
        if discounted_price is not None and base_price is not None and discounted_price > base_price:
            raise serializers.ValidationError({"discounted_price": "Discounted price cannot be greater than base price."})
        return attrs