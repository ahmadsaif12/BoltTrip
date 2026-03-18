from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import TourPackageViewSet, TourTypeViewSet

router = SimpleRouter()
router.register(r"packages", TourPackageViewSet, basename="packages")
router.register(r"package-types", TourTypeViewSet, basename="package-types")

urlpatterns = [
    path("", include(router.urls)),
]
