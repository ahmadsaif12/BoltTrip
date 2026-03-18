from django.contrib import admin

from .models import Airline, Airport, Flight, FlightRoute, FlightSearch


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ("name", "iata_code", "icao_code", "created_at")
    search_fields = ("name", "iata_code", "icao_code")


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country", "iata_code", "icao_code")
    search_fields = ("name", "city", "country", "iata_code", "icao_code")


@admin.register(FlightRoute)
class FlightRouteAdmin(admin.ModelAdmin):
    list_display = ("origin", "destination", "created_at")
    search_fields = ("origin__city", "origin__iata_code", "destination__city", "destination__iata_code")


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "flight_number",
        "airline",
        "route",
        "departure_time",
        "arrival_time",
        "base_price",
        "currency",
        "is_active",
    )
    search_fields = ("flight_number", "airline__name")
    list_filter = ("airline", "currency", "is_active", "is_refundable")


@admin.register(FlightSearch)
class FlightSearchAdmin(admin.ModelAdmin):
    list_display = ("trip_type", "origin", "destination", "departure_date", "return_date", "travelers")
    search_fields = ("origin__city", "destination__city", "origin__iata_code", "destination__iata_code")
    list_filter = ("trip_type",)
