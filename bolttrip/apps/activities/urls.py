from django.urls import path

from .views import ActivityCategoryViewSet, ActivityViewSet

urlpatterns = [
    path(
        "",
        ActivityViewSet.as_view({"get": "list", "post": "create"}),
        name="activity-list",
    ),
    path(
        "featured/",
        ActivityViewSet.as_view({"get": "featured"}),
        name="activity-featured",
    ),
    path(
        "<int:pk>/",
        ActivityViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        name="activity-detail",
    ),
    path(
        "categories/",
        ActivityCategoryViewSet.as_view({"get": "list"}),
        name="activity-category-list",
    ),
    path(
        "categories/featured/",
        ActivityCategoryViewSet.as_view({"get": "featured"}),
        name="activity-category-featured",
    ),
    path(
        "categories/<int:pk>/",
        ActivityCategoryViewSet.as_view({"get": "retrieve"}),
        name="activity-category-detail",
    ),
]
