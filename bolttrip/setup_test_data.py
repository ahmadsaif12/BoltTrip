import os
import django
import datetime
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bolttrip.settings')
django.setup()

from apps.users.models import User
from apps.bookings.models import Booking
from apps.packages.models import TravelPackage, Destination

# Create/get test user
user, created = User.objects.get_or_create(
    email='test@example.com',
    defaults={
        'name': 'Test User',
        'is_active': True,
        'is_verified': True,
    }
)
user.set_password('TestPass@123')
user.save()
print(f"User: {user.email} - Created: {created}")

# Get or create a destination
destination = Destination.objects.first()
if not destination:
    destination = Destination.objects.create(
        name='Kathmandu',
        slug='kathmandu',
    )
    print(f"Created test destination: {destination.name}")
else:
    print(f"Using existing destination: {destination.name}")

# Get or create a travel package
package = TravelPackage.objects.filter(destination=destination).first()
if not package:
    package = TravelPackage.objects.create(
        title='Test Package',
        short_description='Test Package for Payment Testing',
        description='Test Package for Payment',
        destination=destination,
        base_price=Decimal('5000.00'),
        duration_days=5,
        location_text='Kathmandu',
        cover_image_url='https://via.placeholder.com/600x400',
    )
    print(f"Created test package: {package.title}")
else:
    print(f"Using existing package: {package.title}")

# Create test booking
booking, created = Booking.objects.get_or_create(
    user=user,
    booking_reference='TEST-001',
    defaults={
        'package': package,
        'booking_type': 'package',
        'booking_status': 'pending',
        'payment_status': 'unpaid',
        'start_date': datetime.date.today(),
        'total_amount': package.base_price,
        'currency': 'USD',
        'contact_name': 'Test User',
        'contact_email': 'test@example.com',
    }
)
print(f"Booking: {booking.booking_reference} - ID: {booking.id} - Created: {created}")
print(f"\n✅ Test data ready!")
print(f"\n📝 Login with:")
print(f"  Email: test@example.com")
print(f"  Password: TestPass@123")
print(f"\n💳 Test payment with booking_id: {booking.id}")


