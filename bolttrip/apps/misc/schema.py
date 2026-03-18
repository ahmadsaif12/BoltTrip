from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view

# -----------------------
# Booking Schemas
# -----------------------
booking_viewset_schema = extend_schema_view(
    list=extend_schema(
        tags=["Bookings"], operation_id="bookings_list",
        summary="List bookings", description="Return the authenticated user's bookings."
    ),
    retrieve=extend_schema(
        tags=["Bookings"], operation_id="bookings_retrieve",
        summary="Retrieve booking", description="Return a single booking owned by the authenticated user."
    ),
    create=extend_schema(
        tags=["Bookings"], operation_id="bookings_create",
        summary="Create booking", description="Create a booking for exactly one target: package, hotel, activity, or guide."
    ),
    partial_update=extend_schema(
        tags=["Bookings"], operation_id="bookings_update",
        summary="Update booking", description="Partially update a booking owned by the authenticated user."
    ),
    destroy=extend_schema(
        tags=["Bookings"], operation_id="bookings_delete",
        summary="Delete booking", description="Delete a booking owned by the authenticated user."
    ),
)

booking_traveler_viewset_schema = extend_schema_view(
    list=extend_schema(
        tags=["Booking Travelers"], operation_id="booking_travelers_list",
        summary="List travelers", description="Return travelers attached to bookings owned by the authenticated user."
    ),
    retrieve=extend_schema(
        tags=["Booking Travelers"], operation_id="booking_travelers_retrieve", summary="Retrieve traveler"
    ),
    create=extend_schema(
        tags=["Booking Travelers"], operation_id="booking_travelers_create",
        summary="Add traveler", description="Attach a traveler to one of the authenticated user's bookings."
    ),
    partial_update=extend_schema(
        tags=["Booking Travelers"], operation_id="booking_travelers_update", summary="Update traveler"
    ),
    destroy=extend_schema(
        tags=["Booking Travelers"], operation_id="booking_travelers_delete", summary="Delete traveler"
    ),
)

booking_payment_viewset_schema = extend_schema_view(
    list=extend_schema(
        tags=["Booking Payments"], operation_id="booking_payments_list",
        summary="List payments", description="Return payments attached to bookings owned by the authenticated user."
    ),
    retrieve=extend_schema(
        tags=["Booking Payments"], operation_id="booking_payments_retrieve", summary="Retrieve payment"
    ),
    create=extend_schema(
        tags=["Booking Payments"], operation_id="booking_payments_create",
        summary="Add payment", description="Attach a payment record to one of the authenticated user's bookings."
    ),
    partial_update=extend_schema(
        tags=["Booking Payments"], operation_id="booking_payments_update", summary="Update payment"
    ),
    destroy=extend_schema(
        tags=["Booking Payments"], operation_id="booking_payments_delete", summary="Delete payment"
    ),
)

# -----------------------
# Activities
# -----------------------
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

# -----------------------
# Content / Stories
# -----------------------
story_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Content Stories"]),
    retrieve=extend_schema(tags=["Content Stories"]),
    create=extend_schema(tags=["Content Stories"]),
    partial_update=extend_schema(tags=["Content Stories"]),
    destroy=extend_schema(tags=["Content Stories"]),
)
story_featured_schema = extend_schema(tags=["Content Stories"])

content_category_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Content Categories"]),
    retrieve=extend_schema(tags=["Content Categories"]),
)

testimonial_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Testimonials"]),
    retrieve=extend_schema(tags=["Testimonials"]),
)
testimonial_featured_schema = extend_schema(tags=["Testimonials"])

faq_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Content FAQ"]),
    retrieve=extend_schema(tags=["Content FAQ"]),
)

promo_banner_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Promo Banners"]),
    retrieve=extend_schema(tags=["Promo Banners"]),
)

newsletter_block_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Newsletter Blocks"]),
    retrieve=extend_schema(tags=["Newsletter Blocks"]),
)

# -----------------------
# Flights
# -----------------------
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

# -----------------------
# Hotels
# -----------------------
hotel_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Hotels"]),
    create=extend_schema(tags=["Hotels"]),
    retrieve=extend_schema(tags=["Hotels"]),
    partial_update=extend_schema(tags=["Hotels"]),
    destroy=extend_schema(tags=["Hotels"]),
)

# Hotel Amenities
hotel_amenities_schema = [
    extend_schema(
        methods=["GET"], tags=["Hotel Amenities"], operation_id="hotel_amenities_list",
        parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)]
    ),
    extend_schema(
        methods=["POST"], tags=["Hotel Amenities"], operation_id="hotel_amenities_create",
        parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)]
    ),
]
hotel_amenity_detail_schema = extend_schema(
    methods=["DELETE"], tags=["Hotel Amenities"], operation_id="hotel_amenities_remove",
    parameters=[
        OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH),
        OpenApiParameter(name="amenity_id", type=int, location=OpenApiParameter.PATH)
    ],
)

# Hotel Rooms
hotel_rooms_schema = [
    extend_schema(
        methods=["GET"], tags=["Hotel Rooms"], operation_id="hotel_rooms_list",
        parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)]
    ),
    extend_schema(
        methods=["POST"], tags=["Hotel Rooms"], operation_id="hotel_rooms_create",
        parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)]
    ),
]
hotel_room_detail_schema = [
    extend_schema(
        methods=["GET"], tags=["Hotel Rooms"], operation_id="hotel_room_retrieve",
        parameters=[
            OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH),
            OpenApiParameter(name="room_id", type=int, location=OpenApiParameter.PATH),
        ]
    ),
    extend_schema(
        methods=["PATCH"], tags=["Hotel Rooms"], operation_id="hotel_room_update",
        parameters=[
            OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH),
            OpenApiParameter(name="room_id", type=int, location=OpenApiParameter.PATH),
        ]
    ),
    extend_schema(
        methods=["DELETE"], tags=["Hotel Rooms"], operation_id="hotel_room_delete",
        parameters=[
            OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH),
            OpenApiParameter(name="room_id", type=int, location=OpenApiParameter.PATH),
        ]
    ),
]

# -----------------------
# Travel Packages / Destinations / Planner
# -----------------------
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

# -----------------------
# User / Auth
# -----------------------
user_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Users"]),
    retrieve=extend_schema(tags=["Users"]),
)
user_register_schema = extend_schema(tags=["Auth"], summary="Register user", description="Create a new user account.")
user_token_login_schema = extend_schema(tags=["Auth"], summary="Login user", description="Authenticate a user and return JWT access and refresh tokens.")
user_token_refresh_schema = extend_schema(tags=["Auth"], summary="Refresh token", description="Refresh a JWT access token using a refresh token.")
user_change_password_schema = extend_schema(tags=["Auth"], summary="Change password", description="Change the authenticated user's password.")
user_otp_request_schema = extend_schema(tags=["Auth"], summary="Request OTP", description="Generate and send an OTP for the given email address.")
user_otp_verify_schema = extend_schema(tags=["Auth"], summary="Verify OTP", description="Verify a previously generated OTP code.")
user_reset_password_request_schema = extend_schema(tags=["Auth"], summary="Request password reset", description="Send a password reset link to the given email address.")
user_reset_password_confirm_schema = extend_schema(tags=["Auth"], summary="Confirm password reset", description="Set a new password using the password reset uid and token.")

user_profile_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["User Profiles"]),
    retrieve=extend_schema(tags=["User Profiles"]),
    create=extend_schema(tags=["User Profiles"]),
    partial_update=extend_schema(tags=["User Profiles"]),
    destroy=extend_schema(tags=["User Profiles"]),
)

guide_profile_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Guide Profiles"]),
    retrieve=extend_schema(tags=["Guide Profiles"]),
)
guide_profile_compare_schema = extend_schema(tags=["Guide Profiles"])
guide_most_booked_schema = extend_schema(
    tags=["Guide Profiles"], summary="Most booked guides",
    description="Return guides ordered by total bookings."
)

wishlist_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Wishlists"]),
    retrieve=extend_schema(tags=["Wishlists"]),
    create=extend_schema(tags=["Wishlists"]),
    partial_update=extend_schema(tags=["Wishlists"]),
    destroy=extend_schema(tags=["Wishlists"]),
)

notification_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Notifications"]),
    retrieve=extend_schema(tags=["Notifications"]),
    create=extend_schema(tags=["Notifications"]),
    partial_update=extend_schema(tags=["Notifications"]),
    destroy=extend_schema(tags=["Notifications"]),
)