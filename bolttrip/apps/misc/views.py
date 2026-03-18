from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import APIHealthSerializer, APIModuleSerializer


class APIHealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = APIHealthSerializer(
            {
                "status": "ok",
                "app": "misc",
            }
        )
        return Response(serializer.data)


class APIModuleListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = APIModuleSerializer(
            [
                {"name": "users", "path": "/api/users/"},
                {"name": "flights", "path": "/api/flights/"},
                {"name": "hotel", "path": "/api/hotel/"},
                {"name": "tours", "path": "/api/tours/"},
                {"name": "packages", "path": "/api/packages/"},
                {"name": "activities", "path": "/api/activities/"},
                {"name": "planner", "path": "/api/planner/"},
                {"name": "content", "path": "/api/content/"},
                {"name": "bookings", "path": "/api/bookings/"},
            ],
            many=True,
        )
        return Response(serializer.data)
