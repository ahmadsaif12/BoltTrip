from django.db import models
from apps.misc.models import BaseModel

# Create your models here.

class Airline(BaseModel):
    name = models.CharField(max_length=120)
    iata_code = models.CharField(max_length=2, blank=True, null=True)
    icao_code = models.CharField(max_length=3, blank=True,null=True)
    logo_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Airport(BaseModel):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=3, unique=True)
    iata_code = models.CharField(max_length=3, unique=True)
    icao_code = models.CharField(max_length=4, blank=True, null=True)
    
    def __str__(self):
        return f"{self.city}{self.iata_code}"
    

class FlightRoute(BaseModel):
    origin = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="routes_from")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE,related_name="flights")

    def __str__(self):
        return f"{self.origin.iata_code} → {self.destination.iata_code}"
        
class Flight(BaseModel):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name="flights")
    route = models.ForeignKey(FlightRoute, on_delete=models.CASCADE, related_name="flights")
    flight_number = models.CharField(max_length=10)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    seats_available = models.PositiveIntegerField(default=0)
    is_refundable = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.airline.name} {self.flight_number}"

class FlightSearch(BaseModel):
    Trip_Type_Choices = [
         ("one_way", "One Way"),
        ("round_trip", "Round Trip"),
        ("multi_city", "Multi City"),
    ]
    
    trip_type = models.CharField(max_length=20, choices=Trip_Type_Choices)
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE,related_name="searches_from")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE,related_name="searches_to")
    departure_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    travelers = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.trip_type}: {self.origin} → {self.destination}"