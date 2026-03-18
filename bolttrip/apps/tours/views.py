from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from apps.misc.schema import (
    tour_package_featured_schema,
    tour_package_viewset_schema,
    tour_type_viewset_schema,
)
from .models import TourPackage, TourType
from .serializers import (
    TourPackageSerializer,
    TourPackageWriteSerializer,
    TourTypeSerializer,
)


@tour_package_viewset_schema
class TourPackageViewSet(viewsets.ModelViewSet):
    queryset = TourPackage.objects.select_related("package_type").filter(is_active=True)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "destination", "country"]
    ordering_fields = ["base_price", "rating", "duration_days", "created_at"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in {"create", "partial_update"}:
            return TourPackageWriteSerializer
        return TourPackageSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    @tour_package_featured_schema
    @action(detail=False, methods=["get"], url_path="featured")
    def featured(self, request):
        queryset = self.get_queryset().filter(is_featured=True)
        serializer = TourPackageSerializer(queryset, many=True)
        return Response(serializer.data)


@tour_type_viewset_schema
class TourTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourType.objects.filter(is_active=True)
    serializer_class = TourTypeSerializer
