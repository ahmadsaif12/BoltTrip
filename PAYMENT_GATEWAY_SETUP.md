# Payment Gateway Setup Guide

This guide explains how to set up eSewa and Khalti payment integration for BoltTrip.

## Payment Methods Added

Your backend now supports:
- **eSewa** (`esewa`) - Free payment gateway for Nepal
- **Khalti** (`khalti`) - Popular mobile wallet in Nepal

## Prerequisites

Both eSewa and Khalti are **free** to integrate:
1. **eSewa**: https://esewa.com.np/ (register merchant account)
2. **Khalti**: https://khalti.com/ (register for API keys)

---

## Setup Instructions

### 1. Add Environment Variables to `.env`

```bash
# eSewa Configuration
ESEWA_MERCHANT_CODE=your_merchant_code
ESEWA_MERCHANT_SECRET_KEY=your_secret_key
ESEWA_PRODUCT_CODE=TRAVEL

# Khalti Configuration
KHALTI_PUBLIC_KEY=your_public_key
KHALTI_SECRET_KEY=your_secret_key

# Frontend URLs
FRONTEND_URL=http://localhost:3000
API_URL=http://localhost:8000
```

### 2. Registering with Providers

#### **eSewa Registration**
1. Go to https://esewa.com.np/
2. Click "Merchant Services" → "Integration"
3. Register as merchant and get:
   - Merchant Code
   - Merchant Secret Key
4. Add them to `.env`

#### **Khalti Registration**
1. Go to https://khalti.com/
2. Go to Settings → API Keys
3. Get:
   - Public Key
   - Secret Key
4. Add them to `.env`

**For Testing**: Use the test credentials in `payment_gateway.py` (they have defaults)

---

## API Endpoints

### 1. **Initiate eSewa Payment**

```
POST /api/bookings/payments/initiate_esewa/
```

**Request:**
```json
{
  "booking_id": 1,
  "amount": 5000
}
```

**Response:**
```json
{
  "gateway": "esewa",
  "transaction_uuid": "uuid-here",
  "url": "https://esewa.com.np/api/epay/main/v2/form",
  "amount": "5000",
  "merchant_code": "EPAYTEST",
  "signature": "signature-hash",
  "product_code": "TRAVEL",
  "success_url": "http://localhost:3000/payment/success",
  "failure_url": "http://localhost:3000/payment/failure",
  ...
}
```

**Frontend Usage:**
```javascript
// 1. Get payment data from backend
const response = await fetch('/api/bookings/payments/initiate_esewa/', {
  method: 'POST',
  body: JSON.stringify({
    booking_id: bookingId,
    amount: totalAmount
  })
});

const paymentData = await response.json();

// 2. Redirect to eSewa with form data
const form = document.createElement('form');
form.method = 'POST';
form.action = paymentData.url;

Object.entries(paymentData).forEach(([key, value]) => {
  const input = document.createElement('input');
  input.type = 'hidden';
  input.name = key;
  input.value = value;
  form.appendChild(input);
});

document.body.appendChild(form);
form.submit();
```

---

### 2. **Initiate Khalti Payment**

```
POST /api/bookings/payments/initiate_khalti/
```

**Request:**
```json
{
  "booking_id": 1,
  "amount": 5000
}
```

**Response:**
```json
{
  "gateway": "khalti",
  "public_key": "your_public_key",
  "amount": 500000,
  "product_identity": "booking_1_abc123",
  "product_name": "Booking BK-ABC123",
  "product_url": "http://localhost:3000/bookings",
  "return_url": "http://localhost:3000/payment/success",
  ...
}
```

**Frontend Usage (using Khalti JavaScript SDK):**
```html
<!-- Include Khalti JS -->
<script src="https://khalti.s3.amazonaws.com/KPG/dist/2.0.0/khalti-checkout.iffe.js"></script>

<script>
  async function initiateKhaltiPayment(bookingId, amount) {
    // 1. Get payment config from backend
    const response = await fetch('/api/bookings/payments/initiate_khalti/', {
      method: 'POST',
      body: JSON.stringify({
        booking_id: bookingId,
        amount: amount
      })
    });
    
    const config = await response.json();
    
    // 2. Initialize Khalti checkout
    let checkout = new KhaltiCheckout({
      publicKey: config.public_key,
      productIdentity: config.product_identity,
      productName: config.product_name,
      productUrl: config.product_url,
      amount: config.amount,
      eventHandler: {
        onSuccess(payload) {
          // Send token to backend for verification
          verifyKhaltiPayment(bookingId, payload.token, config.amount);
        },
        onError(error) {
          console.error('Payment failed:', error);
        },
        onClose() {
          console.log('Payment cancelled');
        }
      }
    });
    
    checkout.show();
  }
  
  async function verifyKhaltiPayment(bookingId, token, amount) {
    const response = await fetch('/api/bookings/payments/verify_khalti/', {
      method: 'POST',
      body: JSON.stringify({
        booking_id: bookingId,
        token: token,
        amount: amount
      })
    });
    
    const result = await response.json();
    if (result.success) {
      console.log('Payment successful!', result.payment);
      // Redirect to success page
      window.location.href = '/payment/success';
    }
  }
</script>
```

---

### 3. **Verify eSewa Payment**

```
POST /api/bookings/payments/verify_esewa/
```

**Request:**
```json
{
  "booking_id": 1,
  "transaction_uuid": "uuid-from-esewa"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Payment verified successfully",
  "payment": {
    "id": 1,
    "booking": 1,
    "transaction_id": "123456",
    "payment_method": "esewa",
    "amount": "5000",
    "payment_status": "paid",
    "paid_at": "2026-03-30T12:30:00Z"
  }
}
```

---

### 4. **Verify Khalti Payment**

```
POST /api/bookings/payments/verify_khalti/
```

**Request:**
```json
{
  "booking_id": 1,
  "token": "khalti-payment-token",
  "amount": 500000
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Payment verified successfully",
  "payment": {
    "id": 2,
    "booking": 1,
    "transaction_id": "khalti-idx-123",
    "payment_method": "khalti",
    "amount": "5000",
    "payment_status": "paid",
    "paid_at": "2026-03-30T12:30:00Z"
  }
}
```

---

## Payment Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React/Vue)                 │
└──────────────────┬──────────────────────────────────────┘
                   │
        1. User clicks "Pay with eSewa"
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│             Backend API (/initiate_esewa/)              │
│  ✓ Verify booking exists                               │
│  ✓ Generate transaction UUID                           │
│  ✓ Generate HMAC signature                             │
│  ✓ Return eSewa form data                              │
└──────────────────┬──────────────────────────────────────┘
                   │
        2. Submit form to eSewa
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│                    eSewa Gateway                        │
│  ✓ User enters credentials                             │
│  ✓ Payment processed                                   │
│  ✓ Redirect to frontend success_url                    │
└──────────────────┬──────────────────────────────────────┘
                   │
        3. Callback with transaction_uuid
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│          Frontend (/payment/success)                    │
│  ✓ Extract transaction_uuid from URL                   │
│  ✓ Send to /verify_esewa/                              │
└──────────────────┬──────────────────────────────────────┘
                   │
        4. Call verify endpoint
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│            Backend API (/verify_esewa/)                 │
│  ✓ Call eSewa API to verify                            │
│  ✓ Create BookingPayment record                        │
│  ✓ Update booking payment_status to PAID               │
│  ✓ Return success response                             │
└─────────────────────────────────────────────────────────┘
```

---

## Testing with Test Credentials

### eSewa Test
```bash
# Already configured in payment_gateway.py
MERCHANT_CODE = "EPAYTEST"
SECRET_KEY = "8gBm/:&EnhH.1/q"

# Use amount: 100 for testing
# A test successful transaction returns ref_id like "0011111"
```

### Khalti Test
```bash
# You need to register for test keys at https://khalti.com
# Test flow works without real wallet
# Khalti provides sandbox environment
```

---

## Database Schema

New payment methods are stored in `BookingPayment` model:

```python
class BookingPayment(BaseModel):
    booking = ForeignKey(Booking)
    payment_method = CharField(choices=['card', 'esewa', 'khalti', ...])
    amount = DecimalField()
    currency = CharField()
    payment_status = CharField(choices=['unpaid', 'paid', 'failed', 'refunded'])
    transaction_id = CharField()  # eSewa ref_id or Khalti idx
    paid_at = DateTimeField()
    notes = TextField()
```

---

## Troubleshooting

### eSewa Payment Not Verifying
- Check `transaction_uuid` is passed correctly from frontend
- Verify `ESEWA_MERCHANT_CODE` matches registered merchant
- Check network request to `https://esewa.com.np/api/epay/transaction/status/`

### Khalti Payment Not Verifying
- Ensure `KHALTI_SECRET_KEY` is correct (starts with "Secret")
- Token should be captured from Khalti checkout's `onSuccess`
- Amount must match original request (in paisa)

### Signature Mismatch for eSewa
- Order of fields must be: `total_amount,transaction_uuid,product_code`
- Verify secret key is exactly correct (no spaces)
- SHA256 hashing is case-sensitive

---

## Production Checklist

Before going live:
- [ ] Register production merchant account with eSewa
- [ ] Get production API keys from Khalti
- [ ] Update `.env` with production keys
- [ ] Set `FRONTEND_URL` to production domain
- [ ] Set `API_URL` to production API domain
- [ ] Test payment flow end-to-end
- [ ] Enable HTTPS (required for payment gateways)
- [ ] Monitor transaction logs in admin panel

---

## File Changes Summary

**New Files:**
- `apps/bookings/payment_gateway.py` - Payment gateway integration

**Modified Files:**
- `apps/bookings/models.py` - Added ESEWA and KHALTI to PaymentMethod choices
- `apps/bookings/views.py` - Added 4 new endpoints for payment initiation and verification

**No Database Migration Needed** - Existing BookingPayment model compatible

---

## Support

For issues:
1. Check error in `docker-compose logs web`
2. Verify environment variables are loaded
3. Test eSewa/Khalti URLs are accessible
4. Check network requests in browser DevTools
