from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    GuideProfileViewSet,
    NotificationViewSet,
    UserProfileViewSet,
    UserViewSet,
    WishlistViewSet,
)

router = SimpleRouter()
router.register(r"me", UserViewSet, basename="users-me")
router.register(r"profiles", UserProfileViewSet, basename="user-profiles")
router.register(r"guides", GuideProfileViewSet, basename="guide-profiles")
router.register(r"wishlists", WishlistViewSet, basename="wishlists")
router.register(r"notifications", NotificationViewSet, basename="notifications")

urlpatterns = [
    path("", include(router.urls)),
]
