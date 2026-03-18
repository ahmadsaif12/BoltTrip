from drf_spectacular.utils import extend_schema, extend_schema_view


activity_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Activities"]),
    retrieve=extend_schema(tags=["Activities"]),
    create=extend_schema(tags=["Activities"]),
    partial_update=extend_schema(tags=["Activities"]),
    destroy=extend_schema(tags=["Activities"]),
)

activity_featured_schema = extend_schema(tags=["Activities"])

activity_category_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Activity Categories"]),
    retrieve=extend_schema(tags=["Activity Categories"]),
)

activity_category_featured_schema = extend_schema(tags=["Activity Categories"])
