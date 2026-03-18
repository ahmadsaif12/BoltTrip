from drf_spectacular.utils import extend_schema, extend_schema_view


tour_package_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Packages"]),
    retrieve=extend_schema(tags=["Packages"]),
    create=extend_schema(tags=["Packages"]),
    partial_update=extend_schema(tags=["Packages"]),
    destroy=extend_schema(tags=["Packages"]),
)

tour_package_featured_schema = extend_schema(tags=["Packages"])

tour_type_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Package Types"]),
    retrieve=extend_schema(tags=["Package Types"]),
)
