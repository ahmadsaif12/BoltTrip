from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import HotelViewSet

router = SimpleRouter()
router.register(r"hotels", HotelViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
