"""
Payment Gateway Integration for eSewa and Khalti
- eSewa: https://esewa.com.np/
- Khalti: https://khalti.com/
"""

import hashlib
import json
import uuid
from typing import Dict, Optional, Any
from decimal import Decimal

import requests
from django.conf import settings


class eSewaPay:
    """eSewa payment integration"""
    
    # Test credentials (use .env for production)
    TEST_MERCHANT_CODE = "EPAYTEST"
    TEST_MERCHANT_SECRET_KEY = "8gBm/:&EnhH.1/q"
    
    PROD_MERCHANT_CODE = getattr(settings, "ESEWA_MERCHANT_CODE", TEST_MERCHANT_CODE)
    PROD_MERCHANT_SECRET_KEY = getattr(settings, "ESEWA_MERCHANT_SECRET_KEY", TEST_MERCHANT_SECRET_KEY)
    
    ESEWA_PAYMENT_URL = "https://esewa.com.np/api/epay/main/v2/form"
    ESEWA_VERIFY_URL = "https://esewa.com.np/api/epay/transaction/status/"
    
    @classmethod
    def generate_signature(cls, data: str, secret_key: str) -> str:
        """Generate HMAC-SHA256 signature for eSewa"""
        return hashlib.sha256((data + secret_key).encode()).hexdigest()
    
    @classmethod
    def initiate_payment(
        cls,
        amount: Decimal,
        transaction_uuid: str,
        product_name: str = "Travel Booking",
        product_code: str = "TRAVEL",
    ) -> Dict[str, Any]:
        """
        Generate eSewa payment form data
        
        Args:
            amount: Payment amount in NPR
            transaction_uuid: Unique transaction ID
            product_name: Name of product/service
            product_code: Code for the product
            
        Returns:
            Dictionary with payment form data and signature
        """
        
        merchant_code = cls.PROD_MERCHANT_CODE
        secret_key = cls.PROD_MERCHANT_SECRET_KEY
        
        # Prepare data for signature
        data = f"total_amount={amount},transaction_uuid={transaction_uuid},product_code={product_code}"
        signature = cls.generate_signature(data, secret_key)
        
        return {
            "url": cls.ESEWA_PAYMENT_URL,
            "amount": str(amount),
            "failure_url": f"{getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')}/payment/failure",
            "product_delivery_charge": "0",
            "product_service_charge": "0",
            "product_code": product_code,
            "product_name": product_name,
            "signed_field_names": "total_amount,transaction_uuid,product_code",
            "success_url": f"{getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')}/payment/success",
            "tax_amount": "0",
            "total_amount": str(amount),
            "transaction_uuid": transaction_uuid,
            "merchant_code": merchant_code,
            "signature": signature,
        }
    
    @classmethod
    def verify_payment(cls, transaction_uuid: str) -> Optional[Dict[str, Any]]:
        """
        Verify eSewa payment status
        
        Args:
            transaction_uuid: Transaction UUID to verify
            
        Returns:
            Payment status dictionary or None if verification fails
        """
        try:
            params = {
                "product_code": getattr(settings, "ESEWA_PRODUCT_CODE", "TRAVEL"),
                "total_amount": "0",  # Set by eSewa
                "transaction_uuid": transaction_uuid,
                "merchant_code": cls.PROD_MERCHANT_CODE,
            }
            
            response = requests.get(
                cls.ESEWA_VERIFY_URL,
                params=params,
                timeout=10,
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": data.get("status") == "COMPLETE",
                    "transaction_id": data.get("ref_id"),
                    "status": data.get("status"),
                    "amount": data.get("total_amount"),
                    "raw_response": data,
                }
        except Exception as e:
            print(f"eSewa verification error: {str(e)}")
        
        return None


class KhaltiPay:
    """Khalti payment integration"""
    
    TEST_PUBLIC_KEY = "test_public_key_123"  # Test key (replace with actual)
    TEST_SECRET_KEY = "test_secret_key_123"   # Test key (replace with actual)
    
    PUBLIC_KEY = getattr(settings, "KHALTI_PUBLIC_KEY", TEST_PUBLIC_KEY)
    SECRET_KEY = getattr(settings, "KHALTI_SECRET_KEY", TEST_SECRET_KEY)
    
    KHALTI_VERIFICATION_URL = "https://khalti.com/api/v2/payment/verify/"
    
    @classmethod
    def initiate_payment(
        cls,
        amount: Decimal,
        product_identity: str,
        product_name: str = "Travel Booking",
        return_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Prepare Khalti payment data
        
        Args:
            amount: Amount in paisa (1 NPR = 100 paisa)
            product_identity: Unique product/transaction ID
            product_name: Name of the product
            return_url: URL to redirect after payment
            
        Returns:
            Dictionary with Khalti payment parameters
        """
        
        amount_in_paisa = int(amount * 100)  # Convert NPR to paisa
        
        return {
            "public_key": cls.PUBLIC_KEY,
            "amount": amount_in_paisa,  # Amount in paisa
            "product_identity": product_identity,
            "product_name": product_name,
            "product_url": f"{getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')}/bookings",
            "eventHandler": {
                "onSuccess": f"{getattr(settings, 'API_URL', 'http://localhost:8000')}/api/bookings/payments/khalti/verify/",
                "onError": f"{getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')}/payment/failure",
                "onClose": f"{getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')}/payment/cancelled",
            },
            "return_url": return_url or f"{getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')}/payment/success",
        }
    
    @classmethod
    def verify_payment(cls, token: str, amount: int) -> Optional[Dict[str, Any]]:
        """
        Verify Khalti payment token
        
        Args:
            token: Khalti payment token from frontend
            amount: Amount in paisa that was charged
            
        Returns:
            Payment verification data or None if verification fails
        """
        try:
            headers = {
                "Authorization": f"Key {cls.SECRET_KEY}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "token": token,
                "amount": amount,
            }
            
            response = requests.post(
                cls.KHALTI_VERIFICATION_URL,
                json=payload,
                headers=headers,
                timeout=10,
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "transaction_id": data.get("idx"),
                    "status": "success",
                    "amount": data.get("amount"),
                    "mobile": data.get("mobile", None),
                    "raw_response": data,
                }
            else:
                print(f"Khalti verification failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Khalti verification error: {str(e)}")
        
        return None


class PaymentGateway:
    """Main payment gateway handler"""
    
    @staticmethod
    def initiate_esewa_payment(
        booking_id: int,
        amount: Decimal,
        product_name: str = "Travel Booking",
    ) -> Dict[str, Any]:
        """Initiate eSewa payment"""
        transaction_uuid = str(uuid.uuid4())
        
        payment_data = eSewaPay.initiate_payment(
            amount=amount,
            transaction_uuid=transaction_uuid,
            product_name=product_name,
        )
        
        return {
            "gateway": "esewa",
            "transaction_uuid": transaction_uuid,
            **payment_data,
        }
    
    @staticmethod
    def initiate_khalti_payment(
        booking_id: int,
        amount: Decimal,
        product_name: str = "Travel Booking",
    ) -> Dict[str, Any]:
        """Initiate Khalti payment"""
        
        product_identity = f"booking_{booking_id}_{uuid.uuid4().hex[:8]}"
        
        payment_data = KhaltiPay.initiate_payment(
            amount=amount,
            product_identity=product_identity,
            product_name=product_name,
        )
        
        return {
            "gateway": "khalti",
            "product_identity": product_identity,
            **payment_data,
        }
    
    @staticmethod
    def verify_esewa_payment(transaction_uuid: str) -> Optional[Dict[str, Any]]:
        """Verify eSewa payment"""
        return eSewaPay.verify_payment(transaction_uuid)
    
    @staticmethod
    def verify_khalti_payment(token: str, amount: int) -> Optional[Dict[str, Any]]:
        """Verify Khalti payment"""
        return KhaltiPay.verify_payment(token, amount)
