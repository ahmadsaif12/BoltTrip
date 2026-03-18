from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import APIHealthSerializer, APIModuleSerializer


class APIHealthView(GenericAPIView):
    serializer_class = APIHealthSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        data = {"status": "ok", "app": "misc"}
        serializer = self.get_serializer(data)
        return Response(serializer.data)


class APIModuleListView(GenericAPIView):
    serializer_class = APIModuleSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        modules = [
            {"name": "users", "path": "/api/users/"},
            {"name": "flights", "path": "/api/flights/"},
            {"name": "hotel", "path": "/api/hotel/"},
            {"name": "tours", "path": "/api/tours/"},
            {"name": "packages", "path": "/api/packages/"},
            {"name": "activities", "path": "/api/activities/"},
            {"name": "planner", "path": "/api/planner/"},
            {"name": "content", "path": "/api/content/"},
            {"name": "bookings", "path": "/api/bookings/"},
        ]
        serializer = self.get_serializer(modules, many=True)
        return Response(serializer.data)