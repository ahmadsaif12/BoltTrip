from decimal import Decimal

from django.core.validators import MinValueValidator,MaxValueValidator
from django.db import models

from apps.misc.models import BaseModel


class TripType(models.TextChoices):
    ONE_WAY = "one_way", "One Way"
    ROUND_TRIP = "round_trip", "Round Trip"
    MULTI_CITY = "multi_city", "Multi City"

class Airline(BaseModel):
    name = models.CharField(max_length=120)
    iata_code = models.CharField(max_length=2, blank=True, null=True)
    icao_code = models.CharField(max_length=3, blank=True,null=True)
    logo_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class Airport(BaseModel):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    iata_code = models.CharField(max_length=3, unique=True)
    icao_code = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        ordering = ["country", "city", "name"]
    
    def __str__(self):
        return f"{self.city} ({self.iata_code})"
    

class FlightRoute(BaseModel):
    origin = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="routes_from")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE,related_name="routes_to")

    class Meta:
        ordering = ["origin__city", "destination__city"]

    def __str__(self):
        return f"{self.origin.iata_code} → {self.destination.iata_code}"
        
class Flight(BaseModel):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name="flights")
    route = models.ForeignKey(FlightRoute, on_delete=models.CASCADE, related_name="flights")
    flight_number = models.CharField(max_length=10)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(1440)])
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    currency = models.CharField(max_length=3, default="USD")
    seats_available = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    is_refundable = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["departure_time", "flight_number"]

    def __str__(self):
        return f"{self.airline.name} {self.flight_number}"

class FlightSearch(BaseModel):
    trip_type = models.CharField(max_length=20, choices=TripType.choices)
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE,related_name="searches_from")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE,related_name="searches_to")
    departure_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    travelers = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(9)])

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.trip_type}: {self.origin} → {self.destination}"
