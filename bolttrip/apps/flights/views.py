from rest_framework import filters, viewsets
from .models import Airline, Airport, Flight, FlightRoute, FlightSearch
from .schema import (
    airline_viewset_schema,
    airport_viewset_schema,
    flight_route_viewset_schema,
    flight_search_viewset_schema,
    flight_viewset_schema,
)
from .serializers import (
    AirlineSerializer,
    AirportSerializer,
    FlightRouteSerializer,
    FlightSearchSerializer,
    FlightSearchWriteSerializer,
    FlightSerializer,
    FlightWriteSerializer,
)


@airline_viewset_schema
class AirlineViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "iata_code", "icao_code"]
    ordering_fields = ["name", "created_at"]


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
    queryset = Flight.objects.select_related("airline", "route__origin", "route__destination").filter(is_active=True)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["flight_number", "airline__name", "route__origin__city", "route__destination__city"]
    ordering_fields = ["departure_time", "arrival_time", "base_price", "created_at"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in {"create", "partial_update"}:
            return FlightWriteSerializer
        return FlightSerializer


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
