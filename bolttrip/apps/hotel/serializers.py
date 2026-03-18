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
