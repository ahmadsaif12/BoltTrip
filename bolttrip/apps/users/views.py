import secrets
from rest_framework.generics import GenericAPIView
from rest_framework import generics, permissions
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

try:
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
    SIMPLEJWT_AVAILABLE = True
except ImportError:
    SIMPLEJWT_AVAILABLE = False

from apps.misc.schema import (
    guide_profile_compare_schema,
    guide_profile_viewset_schema,
    guide_most_booked_schema,
    user_change_password_schema,
    user_otp_request_schema,
    user_otp_verify_schema,
    user_register_schema,
    user_reset_password_confirm_schema,
    user_reset_password_request_schema,
    user_token_login_schema,
    user_token_refresh_schema,
    notification_viewset_schema,
    user_profile_viewset_schema,
    user_viewset_schema,
    wishlist_viewset_schema,
)

from .models import GuideProfile, Notification, User, UserOTP, UserPreference, UserProfile, Wishlist
from .serializers import (
    ChangePasswordSerializer,
    GuideProfileCompareSerializer,
    GuideProfileSerializer,
    LoginSerializer,
    MostBookedGuideSerializer,
    NotificationSerializer,
    OTPRequestSerializer,
    OTPVerifySerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    UserOTPSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    WishlistSerializer,UserPreferenceSerializer
)
from .tasks import send_email_task, send_otp_email_task

@user_register_schema
class UserRegistrationView(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=False)
        otp = f"{secrets.randbelow(1000000):06d}"
        UserOTP.objects.filter(user=user, is_verified=False).delete()
        otp_record = UserOTP.objects.create(user=user, otp=otp)
        send_otp_email_task.delay(user.email, otp)
        return Response(
            {
                "message": "User registered successfully. Please check your email for the OTP to activate your account.",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )

@user_token_login_schema
class UserTokenObtainPairView(GenericAPIView if not SIMPLEJWT_AVAILABLE else TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer if not SIMPLEJWT_AVAILABLE else None

    if not SIMPLEJWT_AVAILABLE:
        def post(self, request):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = authenticate(
                request,
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
            if not user:
                return Response({"detail": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)
            if not user.is_active:
                return Response({"detail": "User account is not activated. Verify your email first."}, status=status.HTTP_403_FORBIDDEN)
            login(request, user)
            return Response(
                {
                    "message": "Login successful.",
                    "jwt_enabled": False,
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )

@user_token_refresh_schema
class UserTokenRefreshView(GenericAPIView if not SIMPLEJWT_AVAILABLE else TokenRefreshView):
    permission_classes = [AllowAny]

    if not SIMPLEJWT_AVAILABLE:
        def post(self, request):
            return Response(
                {"detail": "Token refresh unavailable because djangorestframework-simplejwt is not installed."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

@user_change_password_schema
class ChangePasswordAPIView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

@user_otp_request_schema
class RequestOTPView(GenericAPIView):
    serializer_class = OTPRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.validated_data["email"])
        otp = f"{secrets.randbelow(1000000):06d}"
        UserOTP.objects.filter(user=user, is_verified=False).delete()
        otp_record = UserOTP.objects.create(user=user, otp=otp)
        send_otp_email_task.delay(user.email, otp)
        return Response(UserOTPSerializer(otp_record).data, status=status.HTTP_201_CREATED)

@user_otp_verify_schema
class VerifyOTPView(GenericAPIView):
    serializer_class = OTPVerifySerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_record = serializer.validated_data["otp_record"]
        otp_record.is_verified = True
        otp_record.save(update_fields=["is_verified", "updated_at"])
        user = otp_record.user
        user.is_active = True
        user.save(update_fields=["is_active"])
        return Response({"message": "OTP verified successfully. You can now log in."}, status=status.HTTP_200_OK)

@user_reset_password_request_schema
class ResetPasswordAPIView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.validated_data["email"])
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = request.build_absolute_uri(f"/api/users/reset-password-confirm/{uidb64}/{token}/")
        send_email_task.delay("BoltTrip Password Reset", f"Use this link to reset your password: {reset_url}", [user.email])
        return Response({"message": "Password reset link sent successfully."}, status=status.HTTP_200_OK)

@user_reset_password_confirm_schema
class ResetPasswordConfirmAPIView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Invalid or expired reset token."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data["password"])
        user.save(update_fields=["password"])
        return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)

@guide_profile_compare_schema
class GuideCompareAPIView(GenericAPIView):
    serializer_class = GuideProfileCompareSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = GuideProfile.objects.select_related("user")
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

@guide_most_booked_schema
class MostBookedGuidesAPIView(GenericAPIView):
    serializer_class = MostBookedGuideSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = GuideProfile.objects.select_related("user").annotate(bookings_count=Count("bookings")).order_by("-bookings_count", "-rating", "-created_at")[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@user_viewset_schema
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=["post"], url_path="logout")
    def logout(self, request):
        logout(request)
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)

@user_profile_viewset_schema
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@guide_profile_viewset_schema
class GuideProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GuideProfile.objects.select_related("user")
    serializer_class = GuideProfileSerializer

    @guide_profile_compare_schema
    @action(detail=False, methods=["get"], url_path="compare")
    def compare(self, request):
        serializer = GuideProfileCompareSerializer(self.get_queryset(), many=True, context={"request": request})
        return Response(serializer.data)

@wishlist_viewset_schema
class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@notification_viewset_schema
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserPreferenceView(generics.RetrieveUpdateAPIView):
    serializer_class = UserPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        preference, _ = UserPreference.objects.get_or_create(user=self.request.user)
        return preference