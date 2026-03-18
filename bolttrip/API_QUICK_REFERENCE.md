# BoltTrip API - Developer Quick Reference

**Last Updated**: March 19, 2026

---

## 🚀 Quick Start

### Base URL
```
Development: http://localhost:8000/api/
Production: https://api.yourdomain.com/api/
```

### Authentication
```bash
# Register
POST /api/users/register/
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "password": "SecurePass123!",
  "user_type": "traveler"
}

# Login & Get JWT Token
POST /api/users/token/
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}

# Response
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

# Use token in headers
Authorization: Bearer {access_token}
```

---

## 📍 API Endpoints Summary

### Users (`/api/users/`)
```bash
POST    /register/           # Create account
POST    /token/              # Get JWT token
POST    /token/refresh/      # Refresh token
GET     /account/            # My profile (auth required)
GET     /profiles/           # User profiles (CRUD)
GET     /guides/             # Guide profiles (CRUD)
GET     /wishlist/           # My wishlist (auth required)
GET     /notifications/      # My notifications (auth required)
```

### Hotels (`/api/hotel/`)
```bash
GET     /hotels/             # List hotels
POST    /hotels/             # Create hotel (admin)
GET     /hotels/{id}/        # Hotel details
PATCH   /hotels/{id}/        # Update hotel (admin)
DELETE  /hotels/{id}/        # Delete hotel (admin)
GET     /hotels/{id}/amenities/        # Hotel amenities
POST    /hotels/{id}/amenities/        # Add amenity (admin)
GET     /hotels/{id}/rooms/            # Hotel rooms
POST    /hotels/{id}/rooms/            # Add room (admin)
```

### Flights (`/api/flights/`)
```bash
GET     /                    # List active flights
POST    /                    # Create flight (admin)
GET     /{id}/               # Flight details
GET     /airlines/           # List airlines
GET     /airports/           # List airports
GET     /routes/             # Flight routes
POST    /searches/           # Search flights
```

### Activities (`/api/activities/`)
```bash
GET     /                    # List activities
POST    /                    # Create activity (admin)
GET     /{id}/               # Activity details
GET     /featured/           # Featured activities
GET     /categories/         # Activity categories
```

### Packages (`/api/packages/`)
```bash
GET     /                    # List packages
POST    /                    # Create package (admin)
GET     /{id}/               # Package details
GET     /featured/           # Featured packages
GET     /destinations/       # Travel destinations
GET     /categories/         # Package categories
```

### Tours (`/api/tours/`)
```bash
GET     /packages/           # List tours
POST    /packages/           # Create tour (admin)
GET     /types/              # Tour types
```

### Bookings (`/api/bookings/`)
```bash
GET     /                    # My bookings (auth required)
POST    /                    # Create booking (auth required)
GET     /{id}/               # Booking details
PATCH   /{id}/               # Update booking
DELETE  /{id}/               # Cancel booking
GET     /travelers/          # My travelers (auth required)
POST    /travelers/          # Add traveler (auth required)
GET     /payments/           # My payments (auth required)
POST    /payments/           # Record payment (auth required)
```

### Travel Plans (`/api/planner/`)
```bash
GET     /plans/              # My plans (auth required)
POST    /plans/              # Create plan (auth required)
GET     /templates/          # Itinerary templates
GET     /templates/featured/ # Featured templates
```

### Content (`/api/content/`)
```bash
GET     /stories/            # Travel stories
GET     /categories/         # Content categories
GET     /testimonials/       # User testimonials
GET     /faqs/               # FAQs
GET     /banners/            # Promo banners
```

---

## 🔍 Common Request Examples

### Search & Filter
```bash
# Search hotels by name
GET /api/hotel/hotels/?search=luxury

# Filter by city
GET /api/hotel/hotels/?search=tokyo

# Order by price
GET /api/hotel/hotels/?ordering=price_per_night

# Pagination
GET /api/hotel/hotels/?page=2
```

### Create Booking
```bash
POST /api/bookings/
{
  "booking_type": "hotel",
  "hotel": 1,
  "start_date": "2026-04-01",
  "end_date": "2026-04-05",
  "travelers_count": 2,
  "total_amount": "500.00",
  "paid_amount": "250.00",
  "currency": "USD",
  "contact_name": "John Doe",
  "contact_email": "john@example.com",
  "contact_phone": "+1234567890"
}

# Response
{
  "id": 1,
  "booking_reference": "BK-A1B2C3D4E5",
  "user": "user-uuid",
  "booking_type": "hotel",
  "booking_status": "pending",
  "payment_status": "unpaid",
  ...
}
```

### Add Travel Companion
```bash
POST /api/bookings/travelers/
{
  "booking": 1,
  "full_name": "Jane Doe",
  "age": 28,
  "gender": "female",
  "nationality": "US",
  "passport_number": "P12345678"
}
```

### Record Payment
```bash
POST /api/bookings/payments/
{
  "booking": 1,
  "payment_method": "card",
  "amount": "250.00",
  "currency": "USD"
}
```

---

## ⚠️ Validation Rules

### Age Field (Bookings, Activities)
- Minimum: 0
- Maximum: 110
- Error: "Age must be 110 or less"

### Ratings (Hotels, Activities, Content)
- Minimum: 0.0
- Maximum: 5.0
- Precision: 1 decimal place
- Error: "Ensure this value is less than or equal to 5.0"

### Prices (All Services)
- Minimum: 0.00
- Maximum: 9999999.99
- Decimals: 2 places (cents)
- Error: "Ensure this value is greater than or equal to 0"

### Durations
- Hours: 1-24
- Days: 1-365
- Minutes (flights): 1-1440

### Capacities
- Group size: 1-500
- Room capacity: 1-20

### Strings
- Name/Title: Max 180 chars
- Description: Max 255 chars
- Email: Valid email format

---

## 🔒 Permission Matrix

| Endpoint | AllowAny | IsAuthenticated | IsAdminUser |
|----------|----------|-----------------|-------------|
| GET Hotels | ✅ | - | - |
| POST Hotels | - | - | ✅ |
| PATCH Hotels | - | - | ✅ |
| DELETE Hotels | - | - | ✅ |
| GET Bookings | - | ✅ | ✅ |
| POST Bookings | - | ✅ | ✅ |
| GET Activities | ✅ | - | - |
| POST Activities | - | - | ✅ |
| POST Stories | - | - | ✅ |

---

## 🆘 Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "Validation failed",
  "errors": {
    "age": ["Age must be 110 or less"]
  }
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error. Please contact support."
}
```

---

## 📊 Response Format

### List Response (with pagination)
```json
{
  "count": 100,
  "next": "http://api.example.com/hotels/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Luxury Hotel",
      "rating": 4.5,
      "price_per_night": 150.00,
      ...
    }
  ]
}
```

### Detail Response
```json
{
  "id": 1,
  "name": "Luxury Hotel",
  "slug": "luxury-hotel",
  "rating": 4.5,
  "price_per_night": 150.00,
  "is_featured": true,
  "created_at": "2026-03-01T10:30:00Z",
  "updated_at": "2026-03-19T15:45:30Z"
}
```

---

## 🔄 Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Successful GET, PATCH |
| 201 | Created - Successful POST |
| 204 | No Content - Successful DELETE |
| 400 | Bad Request - Validation failed |
| 401 | Unauthorized - No auth token |
| 403 | Forbidden - No permission |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Server Error - Internal error |

---

## 🛠️ Rate Limiting

- **Anonymous Users**: 100 requests/hour
- **Authenticated Users**: 1000 requests/hour

Limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1234567890
```

---

## 📅 Pagination

Default page size: 20 results

```bash
# Get page 2
GET /api/hotels/hotels/?page=2

# Custom page size (if supported)
GET /api/hotels/hotels/?page_size=50
```

---

## 🔐 Security Best Practices

1. **Never commit credentials**
   - Use environment variables
   - Use `.env.example` as template

2. **Token Management**
   - Store tokens securely (not localStorage)
   - Use httpOnly cookies if possible
   - Refresh tokens before expiry

3. **API Keys**
   - Rotate regularly
   - Never expose in URLs
   - Use headers (Authorization)

4. **HTTPS**
   - Always use HTTPS in production
   - SSLRedirect enabled

5. **CORS**
   - Configured for specific origins only
   - Not `*` in production

---

## 🚀 Common Integration Steps

### 1. Setup
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### 2. Run Development Server
```bash
python manage.py runserver
```

### 3. Access API
- Swagger UI: http://localhost:8000/api/docs/
- Admin Panel: http://localhost:8000/admin/
- API Root: http://localhost:8000/api/

### 4. Test Endpoint
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8000/api/bookings/
```

---

## 📚 Documentation

- **Full API Docs**: `/api/docs/`
- **OpenAPI Schema**: `/api/schema/`
- **Admin Panel**: `/admin/`
- **GitHub**: [Your repo URL]

---

## 🐛 Troubleshooting

### "Invalid token"
- Token expired → Use refresh endpoint
- Wrong format → Must use `Bearer {token}`
- Token invalid → Re-authenticate

### "Permission denied"
- Need admin → Contact administrator
- Not authenticated → Login first
- User scoped → Check user ownership

### "Validation failed"
- Check decimal places (prices: 2, ratings: 1)
- Check value ranges (age 0-110, rating 0-5)
- Check required fields

### "Rate limit exceeded"
- Wait before making more requests
- Check X-RateLimit headers
- Upgrade account tier if needed

---

## 📞 Support

- **Email**: support@bolttrip.com
- **Docs**: https://docs.bolttrip.com
- **Status**: https://status.bolttrip.com
- **Issues**: Report in GitHub issues

---

**Version**: 1.0.0  
**Last Updated**: March 19, 2026  
**Status**: ✅ Production Ready
