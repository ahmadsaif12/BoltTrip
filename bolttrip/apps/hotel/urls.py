from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AmenityViewSet, HotelViewSet, RoomTypeViewSet

router = DefaultRouter()
router.register(r"amenities", AmenityViewSet)
router.register(r"hotels", HotelViewSet)
router.register(r"rooms", RoomTypeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
