from django.urls import path

from .views import AirlineViewSet, AirportViewSet, FlightRouteViewSet, FlightSearchViewSet, FlightViewSet

urlpatterns = [
    path(
        "",
        FlightViewSet.as_view({"get": "list", "post": "create"}),
        name="flight-list",
    ),
    path(
        "<int:pk>/",
        FlightViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        name="flight-detail",
    ),
    path(
        "airlines/",
        AirlineViewSet.as_view({"get": "list", "post": "create"}),
        name="airline-list",
    ),
    path(
        "airlines/<int:pk>/",
        AirlineViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        name="airline-detail",
    ),
    path(
        "airports/",
        AirportViewSet.as_view({"get": "list"}),
        name="airport-list",
    ),
    path(
        "airports/<int:pk>/",
        AirportViewSet.as_view({"get": "retrieve"}),
        name="airport-detail",
    ),
    path(
        "routes/",
        FlightRouteViewSet.as_view({"get": "list"}),
        name="flight-route-list",
    ),
    path(
        "routes/<int:pk>/",
        FlightRouteViewSet.as_view({"get": "retrieve"}),
        name="flight-route-detail",
    ),
    path(
        "searches/",
        FlightSearchViewSet.as_view({"get": "list", "post": "create"}),
        name="flight-search-list",
    ),
    path(
        "searches/<int:pk>/",
        FlightSearchViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        name="flight-search-detail",
    ),
]
