from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.misc.schema import (
    guide_profile_compare_schema,
    guide_profile_viewset_schema,
    notification_viewset_schema,
    user_profile_viewset_schema,
    user_viewset_schema,
    wishlist_viewset_schema,
)

from .models import GuideProfile, Notification, User, UserProfile, Wishlist
from .serializers import (
    GuideProfileCompareSerializer,
    GuideProfileSerializer,
    NotificationSerializer,
    UserProfileSerializer,
    UserSerializer,
    WishlistSerializer,
)


@user_viewset_schema
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


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
