from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from apps.misc.schema import (
    hotel_amenities_schema,
    hotel_amenity_detail_schema,
    hotel_room_detail_schema,
    hotel_rooms_schema,
    hotel_viewset_schema,
)
from .models import Amenity, Hotel, RoomType
from .serializers import (
    AmenitySerializer,
    AmenityWriteSerializer,
    HotelSerializer,
    HotelWriteSerializer,
    RoomTypeSerializer,
    RoomTypeWriteSerializer,
)


@hotel_viewset_schema
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.prefetch_related("amenities", "rooms")
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "city", "country", "property_type"]
    ordering_fields = ["price_per_night", "rating", "created_at"]

    def get_serializer_class(self):
        if self.action in {"create", "partial_update"}:
            return HotelWriteSerializer
        return HotelSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    @hotel_amenities_schema[0]
    @hotel_amenities_schema[1]
    @action(detail=True, methods=["get", "post"], url_path="amenities")
    def amenities(self, request, pk=None):
        hotel = self.get_object()

        if request.method == "GET":
            serializer = AmenitySerializer(hotel.amenities.all(), many=True)
            return Response(serializer.data)

        serializer = AmenityWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amenity = serializer.save()
        hotel.amenities.add(amenity)
        return Response(AmenitySerializer(amenity).data, status=status.HTTP_201_CREATED)

    @hotel_amenity_detail_schema
    @action(detail=True, methods=["delete"], url_path=r"amenities/(?P<amenity_id>[^/.]+)")
    def amenity_detail(self, request, pk=None, amenity_id=None):
        hotel = self.get_object()
        amenity = get_object_or_404(hotel.amenities.all(), pk=amenity_id)

        hotel.amenities.remove(amenity)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @hotel_rooms_schema[0]
    @hotel_rooms_schema[1]
    @action(detail=True, methods=["get", "post"], url_path="rooms")
    def rooms(self, request, pk=None):
        hotel = self.get_object()

        if request.method == "GET":
            serializer = RoomTypeSerializer(hotel.rooms.all(), many=True)
            return Response(serializer.data)

        serializer = RoomTypeWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room = serializer.save(hotel=hotel)
        return Response(RoomTypeSerializer(room).data, status=status.HTTP_201_CREATED)

    @hotel_room_detail_schema[0]
    @hotel_room_detail_schema[1]
    @hotel_room_detail_schema[2]
    @action(detail=True, methods=["get", "patch", "delete"], url_path=r"rooms/(?P<room_id>[^/.]+)")
    def room_detail(self, request, pk=None, room_id=None):
        hotel = self.get_object()
        room = get_object_or_404(hotel.rooms.all(), pk=room_id)

        if request.method == "GET":
            return Response(RoomTypeSerializer(room).data)

        if request.method == "DELETE":
            room.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = RoomTypeWriteSerializer(room, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(hotel=hotel)
        return Response(RoomTypeSerializer(room).data)
