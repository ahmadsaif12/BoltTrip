from decimal import Decimal
from rest_framework import serializers
from .models import Airline, Airport, Flight, FlightRoute, FlightSearch


class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = [
            "id",
            "name",
            "iata_code",
            "icao_code",
            "logo_url",
        ]


class AirlineWriteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=120, required=True)
    iata_code = serializers.CharField(max_length=2, required=False, allow_blank=True)
    icao_code = serializers.CharField(max_length=3, required=False, allow_blank=True)
    logo_url = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Airline
        fields = [
            "id",
            "name",
            "iata_code",
            "icao_code",
            "logo_url",
        ]
        read_only_fields = ["id"]

    def validate_name(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Airline name cannot be empty.")
        return value


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = [
            "id",
            "name",
            "city",
            "country",
            "iata_code",
            "icao_code",
        ]

class FlightRouteSerializer(serializers.ModelSerializer):
    origin = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)

    class Meta:
        model = FlightRoute
        fields = [
            "id",
            "origin",
            "destination",
        ]

class FlightSerializer(serializers.ModelSerializer):
    airline = AirlineSerializer(read_only=True)
    route = FlightRouteSerializer(read_only=True)
    duration_minutes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = [
            "id",
            "airline",
            "route",
            "flight_number",
            "departure_time",
            "arrival_time",
            "duration_minutes",
            "base_price",
            "currency",
            "seats_available",
            "is_refundable",
            "is_active",
            "created_at",
            "updated_at",
        ]

class FlightWriteSerializer(serializers.ModelSerializer):
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0.00"))
    currency = serializers.CharField(min_length=3, max_length=3)
    seats_available = serializers.IntegerField(min_value=0)
    duration_minutes = serializers.IntegerField(min_value=1)

    class Meta:
        model = Flight
        fields = [
            "id",
            "airline",
            "route",
            "flight_number",
            "departure_time",
            "arrival_time",
            "duration_minutes",
            "base_price",
            "currency",
            "seats_available",
            "is_refundable",
            "is_active",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        departure_time = attrs.get("departure_time", getattr(self.instance, "departure_time", None))
        arrival_time = attrs.get("arrival_time", getattr(self.instance, "arrival_time", None))
        if departure_time and arrival_time and arrival_time <= departure_time:
            raise serializers.ValidationError({"arrival_time": "Arrival time must be after departure time."})
        if "currency" in attrs and attrs["currency"]:
            attrs["currency"] = attrs["currency"].upper()
        return attrs

class FlightSearchSerializer(serializers.ModelSerializer):
    origin = AirportSerializer()
    destination = AirportSerializer()

    class Meta:
        model = FlightSearch
        fields = [
            "id",
            "trip_type",
            "origin",
            "destination",
            "departure_date",
            "return_date",
            "travelers",
            "created_at",
            "updated_at",
        ]


class FlightSearchWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightSearch
        fields = [
            "id",
            "trip_type",
            "origin",
            "destination",
            "departure_date",
            "return_date",
            "travelers",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        trip_type = attrs.get("trip_type", getattr(self.instance, "trip_type", None))
        departure_date = attrs.get("departure_date", getattr(self.instance, "departure_date", None))
        return_date = attrs.get("return_date", getattr(self.instance, "return_date", None))

        if trip_type == "round_trip" and not return_date:
            raise serializers.ValidationError({"return_date": "Return date is required for round trips."})
        if departure_date and return_date and return_date < departure_date:
            raise serializers.ValidationError({"return_date": "Return date cannot be earlier than departure date."})
        return attrs