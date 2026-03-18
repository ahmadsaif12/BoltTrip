from django.urls import path

from .views import APIHealthView, APIModuleListView

urlpatterns = [
    path("health/", APIHealthView.as_view(), name="misc-health"),
    path("modules/", APIModuleListView.as_view(), name="misc-modules"),
]
