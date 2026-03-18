from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import (
    ItineraryTemplateViewSet,
    PlannerFaqViewSet,
    SmartSuggestionViewSet,
    TravelPlanViewSet,
)

router = SimpleRouter()
router.register(r"templates", ItineraryTemplateViewSet, basename="planner-templates")
router.register(r"plans", TravelPlanViewSet, basename="travel-plans")
router.register(r"suggestions", SmartSuggestionViewSet, basename="planner-suggestions")
router.register(r"faqs", PlannerFaqViewSet, basename="planner-faqs")

urlpatterns = [
    path("", include(router.urls)),
]
