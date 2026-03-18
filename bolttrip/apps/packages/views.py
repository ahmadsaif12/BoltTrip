from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.misc.schema import (
    destination_featured_schema,
    destination_viewset_schema,
    package_category_viewset_schema,
    travel_package_featured_schema,
    travel_package_viewset_schema,
)
from .models import Destination, PackageCategory, TravelPackage
from .serializers import (
    DestinationSerializer,
    PackageCategorySerializer,
    TravelPackageSerializer,
    TravelPackageWriteSerializer,
)


@travel_package_viewset_schema
class TravelPackageViewSet(viewsets.ModelViewSet):
    queryset = TravelPackage.objects.select_related("category", "destination").filter(is_active=True)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "destination__name", "destination__country", "location_text"]
    ordering_fields = ["base_price", "rating", "duration_days", "created_at"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in {"create", "partial_update"}:
            return TravelPackageWriteSerializer
        return TravelPackageSerializer

    @travel_package_featured_schema
    @action(detail=False, methods=["get"], url_path="featured")
    def featured(self, request):
        queryset = self.get_queryset().filter(is_featured=True)
        serializer = TravelPackageSerializer(queryset, many=True)
        return Response(serializer.data)


@destination_viewset_schema
class DestinationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Destination.objects.filter(is_active=True)
    serializer_class = DestinationSerializer

    @destination_featured_schema
    @action(detail=False, methods=["get"], url_path="featured")
    def featured(self, request):
        serializer = self.get_serializer(self.get_queryset().filter(is_featured=True), many=True)
        return Response(serializer.data)


@package_category_viewset_schema
class PackageCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PackageCategory.objects.filter(is_active=True)
    serializer_class = PackageCategorySerializer
