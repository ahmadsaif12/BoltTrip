from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view


hotel_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Hotels"]),
    create=extend_schema(tags=["Hotels"]),
    retrieve=extend_schema(tags=["Hotels"]),
    partial_update=extend_schema(tags=["Hotels"]),
    destroy=extend_schema(tags=["Hotels"]),
)

hotel_amenities_schema = [
    extend_schema(
        methods=["GET"],
        tags=["Hotel Amenities"],
        operation_id="hotel_amenities_list",
        parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)],
    ),
    extend_schema(
        methods=["POST"],
        tags=["Hotel Amenities"],
        operation_id="hotel_amenities_create",
        parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)],
    ),
]

hotel_amenity_detail_schema = extend_schema(
    methods=["DELETE"],
    tags=["Hotel Amenities"],
    operation_id="hotel_amenities_remove",
    parameters=[
        OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH),
        OpenApiParameter(name="amenity_id", type=int, location=OpenApiParameter.PATH),
    ],
)

hotel_rooms_schema = [
    extend_schema(
        methods=["GET"],
        tags=["Hotel Rooms"],
        operation_id="hotel_rooms_list",
        parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)],
    ),
    extend_schema(
        methods=["POST"],
        tags=["Hotel Rooms"],
        operation_id="hotel_rooms_create",
        parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)],
    ),
]

hotel_room_detail_schema = [
    extend_schema(
        methods=["GET"],
        tags=["Hotel Rooms"],
        operation_id="hotel_room_retrieve",
        parameters=[
            OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH),
            OpenApiParameter(name="room_id", type=int, location=OpenApiParameter.PATH),
        ],
    ),
    extend_schema(
        methods=["PATCH"],
        tags=["Hotel Rooms"],
        operation_id="hotel_room_update",
        parameters=[
            OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH),
            OpenApiParameter(name="room_id", type=int, location=OpenApiParameter.PATH),
        ],
    ),
    extend_schema(
        methods=["DELETE"],
        tags=["Hotel Rooms"],
        operation_id="hotel_room_delete",
        parameters=[
            OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH),
            OpenApiParameter(name="room_id", type=int, location=OpenApiParameter.PATH),
        ],
    ),
]
