from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.misc.schema import (
    itinerary_template_featured_schema,
    itinerary_template_viewset_schema,
    planner_faq_viewset_schema,
    smart_suggestion_viewset_schema,
    travel_plan_viewset_schema,
)
from .models import ItineraryTemplate, PlannerFaq, SmartSuggestion, TravelPlan
from .serializers import (
    ItineraryTemplateSerializer,
    PlannerFaqSerializer,
    SmartSuggestionSerializer,
    TravelPlanSerializer,
    TravelPlanWriteSerializer,
)


@itinerary_template_viewset_schema
class ItineraryTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ItineraryTemplate.objects.filter(is_active=True)
    serializer_class = ItineraryTemplateSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "destination", "country"]
    ordering_fields = ["base_price", "rating", "start_date", "created_at"]

    @itinerary_template_featured_schema
    @action(detail=False, methods=["get"], url_path="featured")
    def featured(self, request):
        serializer = self.get_serializer(self.get_queryset().filter(is_featured=True), many=True)
        return Response(serializer.data)


@travel_plan_viewset_schema
class TravelPlanViewSet(viewsets.ModelViewSet):
    queryset = TravelPlan.objects.select_related("based_on_template").prefetch_related("days__items")
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "destination", "country"]
    ordering_fields = ["start_date", "created_at"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        if not getattr(self.request, "user", None) or not self.request.user.is_authenticated:
            return TravelPlan.objects.none()
        return (
            self.queryset.filter(user=self.request.user)
        )

    def get_serializer_class(self):
        if self.action in {"create", "partial_update"}:
            return TravelPlanWriteSerializer
        return TravelPlanSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@smart_suggestion_viewset_schema
class SmartSuggestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SmartSuggestion.objects.filter(is_active=True)
    serializer_class = SmartSuggestionSerializer


@planner_faq_viewset_schema
class PlannerFaqViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlannerFaq.objects.filter(is_active=True)
    serializer_class = PlannerFaqSerializer
