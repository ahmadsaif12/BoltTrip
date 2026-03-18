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


class FlightSearchSerializer(serializers.ModelSerializer):
    origin = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)

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
