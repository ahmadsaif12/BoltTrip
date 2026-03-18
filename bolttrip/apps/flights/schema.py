from drf_spectacular.utils import extend_schema, extend_schema_view


airline_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Flights Airlines"]),
    retrieve=extend_schema(tags=["Flights Airlines"]),
)

airport_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Flights Airports"]),
    retrieve=extend_schema(tags=["Flights Airports"]),
)

flight_route_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Flights Routes"]),
    retrieve=extend_schema(tags=["Flights Routes"]),
)

flight_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Flights"]),
    retrieve=extend_schema(tags=["Flights"]),
    create=extend_schema(tags=["Flights"]),
    partial_update=extend_schema(tags=["Flights"]),
    destroy=extend_schema(tags=["Flights"]),
)

flight_search_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Flight Searches"]),
    retrieve=extend_schema(tags=["Flight Searches"]),
    create=extend_schema(tags=["Flight Searches"]),
    partial_update=extend_schema(tags=["Flight Searches"]),
    destroy=extend_schema(tags=["Flight Searches"]),
)
