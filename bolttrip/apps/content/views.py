from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.misc.schema import (
    content_category_viewset_schema,
    faq_viewset_schema,
    newsletter_block_viewset_schema,
    promo_banner_viewset_schema,
    story_featured_schema,
    story_viewset_schema,
    testimonial_featured_schema,
    testimonial_viewset_schema,
)
from .models import ContentCategory, FAQ, NewsletterBlock, PromoBanner, Story, Testimonial
from .serializers import (
    ContentCategorySerializer,
    FAQSerializer,
    NewsletterBlockSerializer,
    PromoBannerSerializer,
    StorySerializer,
    StoryWriteSerializer,
    TestimonialSerializer,
)


@story_viewset_schema
class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.select_related("category").filter(is_active=True)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "destination", "country", "summary"]
    ordering_fields = ["published_at", "created_at", "read_time_minutes"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in {"create", "partial_update"}:
            return StoryWriteSerializer
        return StorySerializer

    @story_featured_schema
    @action(detail=False, methods=["get"], url_path="featured")
    def featured(self, request):
        serializer = StorySerializer(self.get_queryset().filter(is_featured=True), many=True)
        return Response(serializer.data)


@content_category_viewset_schema
class ContentCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContentCategory.objects.filter(is_active=True)
    serializer_class = ContentCategorySerializer


@testimonial_viewset_schema
class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Testimonial.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer

    @testimonial_featured_schema
    @action(detail=False, methods=["get"], url_path="featured")
    def featured(self, request):
        serializer = self.get_serializer(self.get_queryset().filter(is_featured=True), many=True)
        return Response(serializer.data)


@faq_viewset_schema
class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer


@promo_banner_viewset_schema
class PromoBannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PromoBanner.objects.filter(is_active=True)
    serializer_class = PromoBannerSerializer


@newsletter_block_viewset_schema
class NewsletterBlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsletterBlock.objects.filter(is_active=True)
    serializer_class = NewsletterBlockSerializer
