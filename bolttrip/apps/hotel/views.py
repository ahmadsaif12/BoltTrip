from rest_framework import viewsets, filters
from .models import Amenity, Hotel, RoomType
from .serializers import AmenitySerializer, HotelSerializer, RoomTypeSerializer

class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name","category"]
    ordering_fields = ["name","created_at"]

class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset =  RoomType.objects.select_related("hotel").prefetch_related("amenities")
    serializer_class = RoomTypeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "hotel__name"]
    ordering_fields = ["price_per_night", "capacity", "created_at"]


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.prefetch_related("amenities", "rooms")
    serializer_class = HotelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "city", "country", "property_type"]
    ordering_fields = ["price_per_night", "rating", "created_at"]