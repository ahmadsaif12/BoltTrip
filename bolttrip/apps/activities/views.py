from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from apps.misc.schema import (
    activity_category_featured_schema,
    activity_category_viewset_schema,
    activity_featured_schema,
    activity_viewset_schema,
)
from .models import Activity, ActivityCategory
from .serializers import (
    ActivityCategorySerializer,
    ActivitySerializer,
    ActivityWriteSerializer,
)


@activity_viewset_schema
class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.select_related("category").filter(is_active=True)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "destination", "country", "location_text"]
    ordering_fields = ["base_price", "rating", "duration_days", "created_at"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in {"create", "partial_update"}:
            return ActivityWriteSerializer
        return ActivitySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    @activity_featured_schema
    @action(detail=False, methods=["get"], url_path="featured")
    def featured(self, request):
        queryset = self.get_queryset().filter(is_featured=True)
        serializer = ActivitySerializer(queryset, many=True)
        return Response(serializer.data)


@activity_category_viewset_schema
class ActivityCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityCategory.objects.filter(is_active=True)
    serializer_class = ActivityCategorySerializer

    @activity_category_featured_schema
    @action(detail=False, methods=["get"], url_path="featured")
    def featured(self, request):
        serializer = self.get_serializer(self.get_queryset().filter(is_featured=True), many=True)
        return Response(serializer.data)
