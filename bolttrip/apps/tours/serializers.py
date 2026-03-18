from decimal import Decimal
from rest_framework import serializers
from .models import TourType, TourPackage


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
    duration_days = serializers.IntegerField(min_value=1)
    duration_nights = serializers.IntegerField(min_value=0)
    group_size = serializers.IntegerField(min_value=1)
    review_count = serializers.IntegerField(min_value=0, required=False)
    base_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal("0.00")
    )
    discounted_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.00"),
        required=False,
        allow_null=True,
    )
    currency = serializers.CharField(min_length=3, max_length=3, required=False)

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

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if "currency" in attrs and attrs["currency"]:
            attrs["currency"] = attrs["currency"].upper()

        base_price = attrs.get("base_price", getattr(self.instance, "base_price", None))
        discounted_price = attrs.get(
            "discounted_price", getattr(self.instance, "discounted_price", None)
        )

        if discounted_price is not None and base_price is not None:
            if discounted_price > base_price:
                raise serializers.ValidationError(
                    {"discounted_price": "Discounted price cannot be greater than base price."}
                )
        return attrs