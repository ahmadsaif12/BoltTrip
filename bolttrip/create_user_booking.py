import os
import django
import datetime
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bolttrip.settings')
django.setup()

from apps.users.models import User
from apps.bookings.models import Booking
from apps.packages.models import TravelPackage, Destination

# Get the authenticated user
user = User.objects.get(email='ahmads87237@gmail.com')
print(f"User: {user.email}")

# Get a test destination
destination = Destination.objects.first()
if not destination:
    destination = Destination.objects.create(name='Kathmandu', slug='kathmandu')

# Get a test package
package = TravelPackage.objects.filter(destination=destination).first()
if not package:
    package = TravelPackage.objects.create(
        title='Popular Package',
        short_description='Test Package',
        description='Test Package Description',
        destination=destination,
        base_price=Decimal('5000.00'),
        duration_days=5,
        location_text='Kathmandu',
        cover_image_url='https://via.placeholder.com/600x400',
    )

# Create booking for user
booking = Booking.objects.create(
    user=user,
    booking_reference=f"BK-{user.id.hex[:8].upper()}",
    package=package,
    booking_type='package',
    booking_status='pending',
    payment_status='unpaid',
    start_date=datetime.date.today(),
    total_amount=package.base_price,
    currency='USD',
    contact_name=user.name,
    contact_email=user.email,
)
print(f"Created booking: {booking.booking_reference} - ID: {booking.id}")
print(f"Amount: {booking.total_amount} {booking.currency}")
