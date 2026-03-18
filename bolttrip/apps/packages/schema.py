from drf_spectacular.utils import extend_schema, extend_schema_view


travel_package_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Packages"]),
    retrieve=extend_schema(tags=["Packages"]),
    create=extend_schema(tags=["Packages"]),
    partial_update=extend_schema(tags=["Packages"]),
    destroy=extend_schema(tags=["Packages"]),
)

travel_package_featured_schema = extend_schema(tags=["Packages"])

destination_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Destinations"]),
    retrieve=extend_schema(tags=["Destinations"]),
)

destination_featured_schema = extend_schema(tags=["Destinations"])

package_category_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Package Categories"]),
    retrieve=extend_schema(tags=["Package Categories"]),
)
