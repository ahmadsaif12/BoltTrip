from django.urls import path

from .views import APIHealthView, APIModuleListView, DashboardView

urlpatterns = [
    path("health/", APIHealthView.as_view(), name="misc-health"),
    path("modules/", APIModuleListView.as_view(), name="misc-modules"),
    path("dashboard/", DashboardView.as_view(), name="misc-dashboard"),
]
