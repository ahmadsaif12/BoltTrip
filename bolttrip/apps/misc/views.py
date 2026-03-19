from datetime import date, timedelta

from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from apps.bookings.models import Booking, BookingStatus, BookingType, PaymentStatus
from apps.hotel.models import RoomType
from apps.misc.schema import dashboard_view_schema
from apps.packages.models import TravelPackage
from apps.users.models import User

from .serializers import (
    APIHealthSerializer,
    APIModuleSerializer,
    DashboardSerializer,
)


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


@dashboard_view_schema
class DashboardView(GenericAPIView):
    """Dashboard stats for hotel bookings and rooms."""

    serializer_class = DashboardSerializer
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = timezone.localdate()

        # Hotel-specific room stats
        bookings = Booking.objects.filter(booking_type=BookingType.HOTEL).exclude(
            booking_status=BookingStatus.CANCELLED
        )
        check_in_today = bookings.filter(start_date=today).count()
        check_out_today = bookings.filter(end_date=today).count()
        in_hotel = (
            bookings.filter(start_date__lte=today)
            .filter(models.Q(end_date__gte=today) | models.Q(end_date__isnull=True))
            .count()
        )

        room_types = RoomType.objects.select_related("hotel").all().order_by("id")
        total_rooms = sum(rt.quantity for rt in room_types)
        occupied_rooms = min(total_rooms, in_hotel)
        available_rooms = max(total_rooms - occupied_rooms, 0)

        room_types_data = [
            {
                "id": rt.id,
                "name": rt.name,
                "hotel": rt.hotel.name,
                "quantity": rt.quantity,
                "deals": 1 if rt.hotel.is_deal else 0,
            }
            for rt in room_types
        ]

        # Overall dashboard stats
        total_bookings = Booking.objects.count()
        total_new_customers = User.objects.filter(
            created_at__gte=today - timedelta(days=30)
        ).count()

        total_earnings = (
            Booking.objects.filter(payment_status=PaymentStatus.PAID)
            .aggregate(total=Sum("paid_amount"))
            .get("total")
            or 0
        )

        def _last_n_months(count: int):
            year = today.year
            month = today.month
            months = []
            for _ in range(count):
                months.append((year, month))
                if month == 1:
                    month = 12
                    year -= 1
                else:
                    month -= 1
            return list(reversed(months))

        revenue_overview = []
        for year, month in _last_n_months(8):
            revenue_total = (
                Booking.objects.filter(
                    payment_status=PaymentStatus.PAID,
                    created_at__year=year,
                    created_at__month=month,
                )
                .aggregate(total=Sum("paid_amount"))
                .get("total")
                or 0
            )
            revenue_overview.append(
                {
                    "month": date(year, month, 1).strftime("%b"),
                    "year": year,
                    "total": revenue_total,
                }
            )

        # Trip overview based on package bookings
        package_bookings = Booking.objects.filter(booking_type=BookingType.PACKAGE)
        total_trips = package_bookings.count()
        cancelled = package_bookings.filter(booking_status=BookingStatus.CANCELLED).count()
        booked = package_bookings.filter(booking_status=BookingStatus.CONFIRMED).count()
        completed = package_bookings.filter(booking_status=BookingStatus.COMPLETED).count()

        def _pct(value: int):
            return round((value / total_trips) * 100, 1) if total_trips else 0.0

        trip_overview = {
            "total_trips": total_trips,
            "cancelled": cancelled,
            "booked": booked,
            "completed": completed,
            "cancelled_percent": _pct(cancelled),
            "booked_percent": _pct(booked),
            "completed_percent": _pct(completed),
        }

        featured_packages = []
        for pkg in TravelPackage.objects.filter(is_active=True).order_by("-rating", "-review_count")[:3]:
            featured_packages.append(
                {
                    "id": pkg.id,
                    "title": pkg.title,
                    "duration_days": pkg.duration_days,
                    "rating": pkg.rating,
                    "review_count": pkg.review_count,
                    "base_price": pkg.base_price,
                    "discounted_price": pkg.discounted_price,
                    "currency": pkg.currency,
                    "cover_image_url": pkg.cover_image_url,
                }
            )

        data = {
            "total_bookings": total_bookings,
            "total_new_customers": total_new_customers,
            "total_earnings": total_earnings,
            "revenue_overview": revenue_overview,
            "trip_overview": trip_overview,
            "featured_packages": featured_packages,
            "check_in_today": check_in_today,
            "check_out_today": check_out_today,
            "in_hotel": in_hotel,
            "total_rooms": total_rooms,
            "occupied_rooms": occupied_rooms,
            "available_rooms": available_rooms,
            "room_types": room_types_data,
        }

        serializer = self.get_serializer(data)
        return Response(serializer.data)