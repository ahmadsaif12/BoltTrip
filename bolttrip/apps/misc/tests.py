import datetime

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.users.models import User
from apps.hotel.models import Hotel, RoomType
from apps.bookings.models import Booking, BookingType

class DashboardAPITest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email="admin@example.com", password="password123", name="Admin"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            city="Test City",
            country="Test Country",
            price_per_night=100,
        )
        RoomType.objects.create(
            hotel=self.hotel,
            name="Single",
            price_per_night=100,
            quantity=10,
        )

        today = timezone.localdate()
        # Booking that checks in today and stays overnight
        Booking.objects.create(
            user=self.admin,
            booking_type=BookingType.HOTEL,
            booking_reference="BK-TEST-1",
            start_date=today,
            end_date=today + datetime.timedelta(days=1),
            total_amount=100,
            paid_amount=0,
            contact_name="Guest 1",
            contact_email="guest1@example.com",
        )
        # Booking that checks out today
        Booking.objects.create(
            user=self.admin,
            booking_type=BookingType.HOTEL,
            booking_reference="BK-TEST-2",
            start_date=today - datetime.timedelta(days=2),
            end_date=today,
            total_amount=200,
            paid_amount=0,
            contact_name="Guest 2",
            contact_email="guest2@example.com",
        )

    def test_dashboard_endpoint_returns_counts(self):
        response = self.client.get("/api/misc/dashboard/")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["check_in_today"], 1)
        self.assertEqual(data["check_out_today"], 1)
        self.assertEqual(data["in_hotel"], 2)
        self.assertEqual(data["total_rooms"], 10)
        self.assertEqual(data["occupied_rooms"], 2)
        self.assertEqual(data["available_rooms"], 8)
        self.assertIsInstance(data["room_types"], list)

        # New dashboard fields
        self.assertEqual(data["total_bookings"], 2)
        self.assertEqual(data["total_new_customers"], 1)
        self.assertEqual(data["total_earnings"], "0.00")
        self.assertIsInstance(data["revenue_overview"], list)
        self.assertEqual(len(data["revenue_overview"]), 8)
        self.assertIsInstance(data["trip_overview"], dict)
        self.assertIsInstance(data["featured_packages"], list)
