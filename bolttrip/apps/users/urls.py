from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ChangePasswordAPIView,
    GuideCompareAPIView,
    GuideProfileViewSet,
    MostBookedGuidesAPIView,
    NotificationViewSet,
    ResetPasswordAPIView,
    ResetPasswordConfirmAPIView,
    RequestOTPView,
    UserPreferenceView,
    UserRegistrationView,
    UserTokenObtainPairView,
    UserTokenRefreshView,
    UserProfileViewSet,
    UserViewSet,
    VerifyOTPView,
    WishlistViewSet,
)

app_name = "user"

router = DefaultRouter()
router.register(r"account", UserViewSet, basename="user")
router.register(r"profiles", UserProfileViewSet, basename="user-profiles")
router.register(r"guides", GuideProfileViewSet, basename="guide-profiles")
router.register(r"wishlist", WishlistViewSet, basename="user-wishlist")
router.register(r"notifications", NotificationViewSet, basename="notifications")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("login/", UserTokenObtainPairView.as_view(), name="user-login"),
    path("token/refresh/", UserTokenRefreshView.as_view(), name="token-refresh"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("request-otp/", RequestOTPView.as_view(), name="request-otp"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset-password"),
    path(
        "reset-password-confirm/<str:uidb64>/<str:token>/",
        ResetPasswordConfirmAPIView.as_view(),
        name="reset-password-confirm",
    ),
    path("guide/compare/", GuideCompareAPIView.as_view(), name="guide-compare"),
    path("guide/most-booked/", MostBookedGuidesAPIView.as_view(), name="most-booked-guide"),
    path("preferences/", UserPreferenceView.as_view(), name="user-preferences"),
]
