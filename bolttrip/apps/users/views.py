import secrets
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status, viewsets
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
    UserTokenObtainPairSerializer,
    WishlistSerializer,
    UserPreferenceSerializer
)
from .tasks import send_email_task

@user_register_schema
class UserRegistrationView(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=False)
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Ye link email mein jayega
        verify_url = request.build_absolute_uri(f"/api/users/verify-email/{uid}/{token}/")
        
        email_body = f"Hi {user.name}, click here to verify and login: {verify_url}"
        send_email_task.delay("Verify Your Account", email_body, [user.email])
        
        return Response(
            {"message": "Registration successful. Please check your email to verify and login."},
            status=status.HTTP_201_CREATED,
        )

# Naya View jo Email click ko handle karke auto-login karega
class VerifyEmailLinkView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid Link"}, status=400)

        if default_token_generator.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save(update_fields=["is_active"])
            return Response(
                {"message": "Email verified. You can now sign in."},
                status=status.HTTP_200_OK,
            )
        return Response({"error": "Link expired"}, status=status.HTTP_400_BAD_REQUEST)

@user_token_login_schema
class UserTokenObtainPairView(GenericAPIView if not SIMPLEJWT_AVAILABLE else TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer if not SIMPLEJWT_AVAILABLE else None

    if not SIMPLEJWT_AVAILABLE:
        def post(self, request):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = authenticate(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
            if not user:
                return Response({"detail": "Invalid credentials."}, status=400)
            if not user.is_active:
                return Response({"detail": "Account not verified."}, status=403)
            return Response({"user": UserSerializer(user).data}, status=200)
    else:
        serializer_class = UserTokenObtainPairSerializer

@user_token_refresh_schema
class UserTokenRefreshView(GenericAPIView if not SIMPLEJWT_AVAILABLE else TokenRefreshView):
    permission_classes = [AllowAny]

@user_change_password_schema
class ChangePasswordAPIView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password changed."}, status=200)

class RequestOTPView(GenericAPIView):
    serializer_class = OTPRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        return Response({"message": "Use the email link sent during registration."}, status=200)

class VerifyOTPView(GenericAPIView):
    serializer_class = OTPVerifySerializer
    permission_classes = [AllowAny]

    def post(self, request):
        return Response({"message": "Please use the direct link in your email."}, status=200)

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
        send_email_task.delay("Password Reset", f"Link: {reset_url}", [user.email])
        return Response({"message": "Reset link sent."}, status=200)

@user_reset_password_confirm_schema
class ResetPasswordConfirmAPIView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except: return Response({"error": "Invalid link"}, status=400)
        
        if default_token_generator.check_token(user, token):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response({"message": "Success"}, status=200)
        return Response({"error": "Invalid token"}, status=400)

@guide_profile_compare_schema
class GuideCompareAPIView(GenericAPIView):
    serializer_class = GuideProfileCompareSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = GuideProfile.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@guide_most_booked_schema
class MostBookedGuidesAPIView(GenericAPIView):
    serializer_class = MostBookedGuideSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = GuideProfile.objects.annotate(bc=Count('bookings')).order_by('-bc')[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return User.objects.filter(id=self.request.user.id)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return UserProfile.objects.filter(user=self.request.user)

class GuideProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GuideProfile.objects.all()
    serializer_class = GuideProfileSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return Wishlist.objects.filter(user=self.request.user)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return Notification.objects.filter(user=self.request.user)

class UserPreferenceView(generics.RetrieveUpdateAPIView):
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        pref, _ = UserPreference.objects.get_or_create(user=self.request.user)
        return pref
