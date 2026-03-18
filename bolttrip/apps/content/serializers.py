from decimal import Decimal
from rest_framework import serializers
from .models import ContentCategory, FAQ, NewsletterBlock, PromoBanner, Story, Testimonial


class ContentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentCategory
        fields = [
            "id",
            "name",
            "slug",
            "description",
        ]


class StorySerializer(serializers.ModelSerializer):
    category = ContentCategorySerializer(read_only=True)

    class Meta:
        model = Story
        fields = [
            "id",
            "title",
            "slug",
            "summary",
            "body",
            "category",
            "cover_image_url",
            "thumbnail_url",
            "destination",
            "country",
            "published_at",
            "read_time_minutes",
            "is_featured",
            "created_at",
            "updated_at",
        ]


class StoryWriteSerializer(serializers.ModelSerializer):
    read_time_minutes = serializers.IntegerField(min_value=1, max_value=240, required=False)

    class Meta:
        model = Story
        fields = [
            "id",
            "title",
            "slug",
            "summary",
            "body",
            "category",
            "cover_image_url",
            "thumbnail_url",
            "destination",
            "country",
            "published_at",
            "read_time_minutes",
            "is_featured",
            "is_active",
            "sort_order",
        ]
        read_only_fields = ["id"]


class TestimonialSerializer(serializers.ModelSerializer):
    rating = serializers.DecimalField(max_digits=2, decimal_places=1, min_value=Decimal("0.0"), max_value=Decimal("5.0"))

    class Meta:
        model = Testimonial
        fields = [
            "id",
            "name",
            "role",
            "location",
            "avatar_url",
            "quote",
            "rating",
            "is_featured",
        ]


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
            "id",
            "question",
            "answer",
            "page",
        ]


class PromoBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoBanner
        fields = [
            "id",
            "title",
            "subtitle",
            "description",
            "image_url",
            "cta_label",
            "cta_url",
            "page",
        ]


class NewsletterBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterBlock
        fields = [
            "id",
            "title",
            "subtitle",
            "image_url",
            "page",
        ]