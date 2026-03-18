from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import AirlineViewSet, AirportViewSet, FlightRouteViewSet, FlightSearchViewSet, FlightViewSet

router = SimpleRouter()
router.register(r"airlines", AirlineViewSet, basename="flight-airlines")
router.register(r"airports", AirportViewSet, basename="flight-airports")
router.register(r"routes", FlightRouteViewSet, basename="flight-routes")
router.register(r"flights", FlightViewSet, basename="flights")
router.register(r"searches", FlightSearchViewSet, basename="flight-searches")

urlpatterns = [
    path("", include(router.urls)),
]
