from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import ActivityCategoryViewSet, ActivityViewSet

router = SimpleRouter()
router.register(r"activities", ActivityViewSet, basename="activities")
router.register(r"categories", ActivityCategoryViewSet, basename="activity-categories")

urlpatterns = [
    path("", include(router.urls)),
]
