from decimal import Decimal
from rest_framework import serializers
from .models import Amenity, Hotel, RoomType


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = [
            "id",
            "name",
            "category",
            "icon_url",
        ]


class AmenityWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = [
            "id",
            "name",
            "category",
            "icon_url",
        ]
        read_only_fields = ["id"]


class RoomTypeSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta:
        model = RoomType
        fields = [
            "id",
            "hotel",
            "name",
            "bed_type",
            "capacity",
            "price_per_night",
            "quantity",
            "room_image_urls",
            "amenities",
        ]


class RoomTypeWriteSerializer(serializers.ModelSerializer):
    capacity = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)
    price_per_night = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0.00"))

    class Meta:
        model = RoomType
        fields = [
            "id",
            "name",
            "bed_type",
            "capacity",
            "price_per_night",
            "quantity",
            "room_image_urls",
            "amenities",
        ]
        read_only_fields = ["id"]


class HotelSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True)
    rooms = RoomTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "property_type",
            "star_rating",
            "rating",
            "review_count",
            "address",
            "city",
            "country",
            "latitude",
            "longitude",
            "phone",
            "email",
            "website",
            "price_per_night",
            "currency",
            "is_deal",
            "deal_price",
            "deal_end_at",
            "main_image_url",
            "gallery_image_urls",
            "check_in_time",
            "check_out_time",
            "is_featured",
            "is_active",
            "amenities",
            "rooms",
            "created_at",
            "updated_at",
        ]


class HotelWriteSerializer(serializers.ModelSerializer):
    star_rating = serializers.IntegerField(min_value=0, max_value=5)
    review_count = serializers.IntegerField(min_value=0, required=False)
    price_per_night = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0.00"))
    deal_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.00"),
        required=False,
        allow_null=True,
    )
    currency = serializers.CharField(min_length=3, max_length=3, required=False)

    class Meta:
        model = Hotel
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "property_type",
            "star_rating",
            "rating",
            "review_count",
            "address",
            "city",
            "country",
            "latitude",
            "longitude",
            "phone",
            "email",
            "website",
            "price_per_night",
            "currency",
            "is_deal",
            "deal_price",
            "deal_end_at",
            "main_image_url",
            "gallery_image_urls",
            "check_in_time",
            "check_out_time",
            "is_featured",
            "is_active",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if "currency" in attrs and attrs["currency"]:
            attrs["currency"] = attrs["currency"].upper()

        is_deal = attrs.get("is_deal", getattr(self.instance, "is_deal", False))
        deal_price = attrs.get("deal_price", getattr(self.instance, "deal_price", None))
        price_per_night = attrs.get("price_per_night", getattr(self.instance, "price_per_night", None))

        if is_deal and not deal_price:
            raise serializers.ValidationError({"deal_price": "Deal price is required when is_deal is enabled."})
        if deal_price is not None and price_per_night is not None and deal_price > price_per_night:
            raise serializers.ValidationError({"deal_price": "Deal price cannot be greater than price per night."})

        return attrs