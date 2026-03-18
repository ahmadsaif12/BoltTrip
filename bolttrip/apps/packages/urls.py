from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import DestinationViewSet, PackageCategoryViewSet, TravelPackageViewSet

router = SimpleRouter()
router.register(r"packages", TravelPackageViewSet, basename="packages")
router.register(r"destinations", DestinationViewSet, basename="destinations")
router.register(r"categories", PackageCategoryViewSet, basename="categories")

urlpatterns = [
    path("", include(router.urls)),
]
