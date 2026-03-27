"""
URL configuration for bolttrip project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.content.views import FAQViewSet
from apps.tours.views import TourTypeViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Backward-compatible aliases (some clients call these without the /api/ prefix)
    path("faqs/", FAQViewSet.as_view({"get": "list"}), name="faqs-alias"),
    path("tour-types/", TourTypeViewSet.as_view({"get": "list"}), name="tour-types-alias"),
    path('api/misc/', include('apps.misc.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/flights/', include('apps.flights.urls')),
    path('api/hotel/', include('apps.hotel.urls')),
    path('api/tours/', include('apps.tours.urls')),
    path('api/packages/', include('apps.packages.urls')),
    path('api/activities/', include('apps.activities.urls')),
    path('api/planner/', include('apps.planner.urls')),
    path('api/content/', include('apps.content.urls')),
    path('api/bookings/', include('apps.bookings.urls')),
]
