from drf_spectacular.utils import extend_schema, extend_schema_view


itinerary_template_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Planner Templates"]),
    retrieve=extend_schema(tags=["Planner Templates"]),
)

itinerary_template_featured_schema = extend_schema(tags=["Planner Templates"])

travel_plan_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Travel Plans"]),
    retrieve=extend_schema(tags=["Travel Plans"]),
    create=extend_schema(tags=["Travel Plans"]),
    partial_update=extend_schema(tags=["Travel Plans"]),
    destroy=extend_schema(tags=["Travel Plans"]),
)

smart_suggestion_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Planner Suggestions"]),
)

planner_faq_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Planner FAQ"]),
)
