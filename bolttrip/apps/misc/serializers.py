from rest_framework import serializers


class APIHealthSerializer(serializers.Serializer):
    status = serializers.CharField()
    app = serializers.CharField()


class APIModuleSerializer(serializers.Serializer):
    name = serializers.CharField()
    path = serializers.CharField()


class DashboardRoomTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    hotel = serializers.CharField()
    quantity = serializers.IntegerField()
    deals = serializers.IntegerField()


class DashboardRevenuePointSerializer(serializers.Serializer):
    month = serializers.CharField()
    year = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=12, decimal_places=2)


class DashboardTripOverviewSerializer(serializers.Serializer):
    total_trips = serializers.IntegerField()
    cancelled = serializers.IntegerField()
    booked = serializers.IntegerField()
    completed = serializers.IntegerField()
    cancelled_percent = serializers.FloatField()
    booked_percent = serializers.FloatField()
    completed_percent = serializers.FloatField()


class DashboardPackageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    duration_days = serializers.IntegerField()
    rating = serializers.DecimalField(max_digits=3, decimal_places=1)
    review_count = serializers.IntegerField()
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    currency = serializers.CharField()
    cover_image_url = serializers.URLField(allow_null=True)


class DashboardSerializer(serializers.Serializer):
    total_bookings = serializers.IntegerField()
    total_new_customers = serializers.IntegerField()
    total_earnings = serializers.DecimalField(max_digits=14, decimal_places=2)
    revenue_overview = DashboardRevenuePointSerializer(many=True)
    trip_overview = DashboardTripOverviewSerializer()
    featured_packages = DashboardPackageSerializer(many=True)

    check_in_today = serializers.IntegerField()
    check_out_today = serializers.IntegerField()
    in_hotel = serializers.IntegerField()
    total_rooms = serializers.IntegerField()
    occupied_rooms = serializers.IntegerField()
    available_rooms = serializers.IntegerField()
    room_types = DashboardRoomTypeSerializer(many=True)
