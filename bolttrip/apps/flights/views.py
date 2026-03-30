from datetime import date
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.misc.schema import (
    airline_viewset_schema,
    airport_viewset_schema,
    flight_route_viewset_schema,
    flight_search_viewset_schema,
    flight_viewset_schema,
)
from .models import Airline, Airport, Flight, FlightRoute, FlightSearch
from .serializers import (
    AirlineSerializer,
    AirlineWriteSerializer,
    AirportSerializer,
    FlightRouteSerializer,
    FlightSearchSerializer,
    FlightSearchWriteSerializer,
    FlightSerializer,
    FlightWriteSerializer,
)


@airline_viewset_schema
class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "iata_code", "icao_code"]
    ordering_fields = ["name", "created_at"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in {"create", "partial_update"}:
            return AirlineWriteSerializer
        return AirlineSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [AllowAny()]


@airport_viewset_schema
class AirportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "city", "country", "iata_code", "icao_code"]
    ordering_fields = ["name", "city", "country", "created_at"]


@flight_route_viewset_schema
class FlightRouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FlightRoute.objects.select_related("origin", "destination")
    serializer_class = FlightRouteSerializer


@flight_viewset_schema
class FlightViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "flight_number",
        "airline__name",
        "route__origin__city",
        "route__origin__iata_code",
        "route__destination__city",
        "route__destination__iata_code",
    ]
    ordering_fields = ["departure_time", "arrival_time", "base_price", "created_at"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        qs = Flight.objects.select_related(
            "airline",
            "route__origin",
            "route__destination",
        ).filter(is_active=True)

        departure_date = self.request.query_params.get("departure_date")
        if departure_date:
            try:
                date.fromisoformat(departure_date)
                qs = qs.filter(departure_time__date=departure_date)
            except ValueError:
                pass

        return qs

    def get_serializer_class(self):
        if self.action in {"create", "partial_update"}:
            return FlightWriteSerializer
        return FlightSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [AllowAny()]


@flight_search_viewset_schema
class FlightSearchViewSet(viewsets.ModelViewSet):
    queryset = FlightSearch.objects.select_related("origin", "destination")
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["origin__city", "destination__city", "trip_type"]
    ordering_fields = ["departure_date", "return_date", "created_at"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in {"create", "partial_update"}:
            return FlightSearchWriteSerializer
        return FlightSearchSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [AllowAny()]