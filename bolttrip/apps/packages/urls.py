from django.urls import path

from .views import DestinationViewSet, PackageCategoryViewSet, TravelPackageViewSet

urlpatterns = [
    path(
        "",
        TravelPackageViewSet.as_view({"get": "list", "post": "create"}),
        name="package-list",
    ),
    path(
        "featured/",
        TravelPackageViewSet.as_view({"get": "featured"}),
        name="package-featured",
    ),
    path(
        "<int:pk>/",
        TravelPackageViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        name="package-detail",
    ),
    path(
        "destinations/",
        DestinationViewSet.as_view({"get": "list"}),
        name="destination-list",
    ),
    path(
        "destinations/featured/",
        DestinationViewSet.as_view({"get": "featured"}),
        name="destination-featured",
    ),
    path(
        "destinations/<int:pk>/",
        DestinationViewSet.as_view({"get": "retrieve"}),
        name="destination-detail",
    ),
    path(
        "categories/",
        PackageCategoryViewSet.as_view({"get": "list"}),
        name="package-category-list",
    ),
    path(
        "categories/<int:pk>/",
        PackageCategoryViewSet.as_view({"get": "retrieve"}),
        name="package-category-detail",
    ),
]
