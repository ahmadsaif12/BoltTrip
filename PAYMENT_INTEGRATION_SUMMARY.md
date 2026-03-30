# BoltTrip Payment Integration - Implementation Summary

## ✅ What's Been Done

### 1. **Added Payment Methods**
- ✅ eSewa payment method added to `BookingPayment` model
- ✅ Khalti payment method added to `BookingPayment` model

### 2. **Created Payment Gateway Module**
- ✅ `apps/bookings/payment_gateway.py` - Full integration with:
  - eSewa API (verification, signature generation)
  - Khalti API (token verification)
  - PaymentGateway utility class

### 3. **Added Backend Endpoints**
Four new API endpoints for payment handling:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/bookings/payments/initiate_esewa/` | Generate eSewa payment form |
| POST | `/api/bookings/payments/initiate_khalti/` | Generate Khalti payment config |
| POST | `/api/bookings/payments/verify_esewa/` | Verify eSewa transaction |
| POST | `/api/bookings/payments/verify_khalti/` | Verify Khalti transaction |

### 4. **Updated Files**
- `apps/bookings/models.py` - Added ESEWA, KHALTI to PaymentMethod choices
- `apps/bookings/views.py` - Added 4 payment action methods
- `requirements.txt` - Added `requests` library

---

## 🚀 Next Steps for Frontend

### 1. **Install Khalti SDK** (for Khalti payments)
```html
<script src="https://khalti.s3.amazonaws.com/KPG/dist/2.0.0/khalti-checkout.iffe.js"></script>
```

### 2. **Create Payment Pages**
```
/payment/success     - Show success message
/payment/failure     - Show error message  
/payment/cancelled   - Show cancellation message
```

### 3. **Implement Payment UI**
Add buttons to booking confirmation page:
```
[Pay with eSewa] [Pay with Khalti] [Other]
```

### 4. **Example: eSewa Integration**
```javascript
// 1. Call backend to get payment form data
const response = await fetch('/api/bookings/payments/initiate_esewa/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    booking_id: bookingId,
    amount: totalAmount
  })
});

const paymentData = await response.json();

// 2. Create and submit form to eSewa
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

// 3. On success page, extract transaction_uuid from URL
const urlParams = new URLSearchParams(window.location.search);
const transactionUuid = urlParams.get('oid');

// 4. Verify payment
const verifyResponse = await fetch('/api/bookings/payments/verify_esewa/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    booking_id: bookingId,
    transaction_uuid: transactionUuid
  })
});

const result = await verifyResponse.json();
if (result.success) {
  console.log('Payment confirmed!', result.payment);
  // Redirect to booking details or success page
}
```

### 5. **Example: Khalti Integration**
```javascript
// 1. Get configuration from backend
const config = await fetch('/api/bookings/payments/initiate_khalti/', {
  method: 'POST',
  body: JSON.stringify({
    booking_id: bookingId,
    amount: totalAmount
  })
}).then(r => r.json());

// 2. Initialize Khalti
const khaltiCheckout = new KhaltiCheckout({
  publicKey: config.public_key,
  productIdentity: config.product_identity,
  productName: config.product_name,
  productUrl: config.product_url,
  amount: config.amount,
  eventHandler: {
    onSuccess(payload) {
      // Verify on backend
      verifyKhalti(bookingId, payload.token, config.amount);
    },
    onError(error) {
      console.error('Payment error:', error);
    }
  }
});

// 3. Show Khalti modal
khaltiCheckout.show();

// 4. Verify payment on backend
async function verifyKhalti(bookingId, token, amount) {
  const result = await fetch('/api/bookings/payments/verify_khalti/', {
    method: 'POST',
    body: JSON.stringify({
      booking_id: bookingId,
      token: token,
      amount: amount
    })
  }).then(r => r.json());
  
  if (result.success) {
    console.log('Payment verified!');
    // Update UI
  }
}
```

---

## 🔧 Environment Variables Required

Add to your `.env` file (optional - test credentials work by default):

```bash
# eSewa
ESEWA_MERCHANT_CODE=your_merchant_code
ESEWA_MERCHANT_SECRET_KEY=your_secret_key
ESEWA_PRODUCT_CODE=TRAVEL

# Khalti
KHALTI_PUBLIC_KEY=your_public_key
KHALTI_SECRET_KEY=your_secret_key

# URLs
FRONTEND_URL=http://localhost:3000
API_URL=http://localhost:8000
```

---

## 📋 API Response Examples

### Initiate eSewa
```bash
curl -X POST http://localhost:8000/api/bookings/payments/initiate_esewa/ \
  -H "Content-Type: application/json" \
  -d '{"booking_id": 1, "amount": 5000}'
```

Response:
```json
{
  "gateway": "esewa",
  "transaction_uuid": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "url": "https://esewa.com.np/api/epay/main/v2/form",
  "amount": "5000",
  "merchant_code": "EPAYTEST",
  "signature": "...",
  "product_code": "TRAVEL",
  ...
}
```

### Verify eSewa Payment
```bash
curl -X POST http://localhost:8000/api/bookings/payments/verify_esewa/ \
  -H "Content-Type: application/json" \
  -d '{
    "booking_id": 1,
    "transaction_uuid": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
  }'
```

Response:
```json
{
  "success": true,
  "message": "Payment verified successfully",
  "payment": {
    "id": 1,
    "booking": 1,
    "transaction_id": "0011111",
    "payment_method": "esewa",
    "amount": "5000",
    "payment_status": "paid",
    "paid_at": "2026-03-30T12:30:00Z"
  }
}
```

---

## 📊 Payment Flow Diagram

```
User Booking
    ↓
[Select Payment Method]
    ↓
    ├─→ eSewa
    │      ↓
    │   Frontend calls /initiate_esewa/
    │      ↓
    │   Backend generates signature & form data
    │      ↓
    │   Frontend submits form to eSewa
    │      ↓
    │   eSewa redirects to success_url with ref_id
    │      ↓
    │   Frontend calls /verify_esewa/
    │      ↓
    │   Backend verifies with eSewa API
    │      ↓
    │   Payment Record Created ✅
    │
    └─→ Khalti
           ↓
        Frontend calls /initiate_khalti/
           ↓
        Backend generates config
           ↓
        Frontend shows Khalti modal
           ↓
        User pays in Khalti modal
           ↓
        Khalti calls onSuccess(payload)
           ↓
        Frontend calls /verify_khalti/
           ↓
        Backend verifies with Khalti API
           ↓
        Payment Record Created ✅
```

---

## 🧪 Testing

### Test with eSewa
1. Use merchant code: `EPAYTEST`
2. Use amount: `100` (minimum)
3. eSewa will return test transaction ref

### Test with Khalti
1. Register at https://khalti.com/
2. Get test API keys
3. Khalti provides sandbox payment flow (no real wallet needed)

---

## 📚 Full Documentation

See [PAYMENT_GATEWAY_SETUP.md](PAYMENT_GATEWAY_SETUP.md) for detailed documentation including:
- Complete setup instructions
- Full API endpoint documentation
- Frontend integration examples
- Troubleshooting guide
- Production checklist

---

## 🎯 Current Status

✅ Backend ready for production
⏳ Waiting for frontend integration

**Backend**: All endpoints working and tested
**Frontend**: Ready to connect to payment endpoints

Your backend API is now payment-ready! 🎉
