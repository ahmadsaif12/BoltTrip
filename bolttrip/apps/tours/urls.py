from django.urls import path

from .views import TourPackageViewSet, TourTypeViewSet

urlpatterns = [
    path(
        "",
        TourPackageViewSet.as_view({"get": "list", "post": "create"}),
        name="tour-package-list",
    ),
    path(
        "featured/",
        TourPackageViewSet.as_view({"get": "featured"}),
        name="tour-package-featured",
    ),
    path(
        "<int:pk>/",
        TourPackageViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        name="tour-package-detail",
    ),
    path(
        "package-types/",
        TourTypeViewSet.as_view({"get": "list"}),
        name="tour-type-list",
    ),
    path(
        "package-types/<int:pk>/",
        TourTypeViewSet.as_view({"get": "retrieve"}),
        name="tour-type-detail",
    ),
]
