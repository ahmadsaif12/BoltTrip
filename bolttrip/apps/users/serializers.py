import re
from rest_framework import serializers
from .models import GuideProfile, Notification, User, UserOTP, UserPreference, UserProfile, Wishlist

def password_validator(value):
    if len(value) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters long.")
    if not re.search(r"\d", value):
        raise serializers.ValidationError("Password must contain at least one digit.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise serializers.ValidationError("Password must contain at least one special character.")
    return value

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "name", "email", "phone", "user_type", "is_staff",
            "is_active", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "is_staff", "is_active", "created_at", "updated_at"]

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[password_validator])

    class Meta:
        model = User
        fields = ["id", "name", "email", "phone", "password", "user_type"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id", "user", "address", "gender", "status", "dob", "bio",
            "nationality", "profile_picture", "preferred_pronouns", "theme",
            "city", "country", "preferred_currency", "preferred_timezone",
            "passport_country", "profile_type", "id_card_number", "kyc_status",
            "emergency_contact", "medical_conditions", "preferred_payment_type",
            "budget_range", "price_sensitivity_level", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class GuideProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GuideProfile
        fields = [
            "id", "user", "travel_company", "profile_photo", "gender", "dob",
            "nationality", "guide_type", "status", "languages_spoken", "specializations",
            "region_expertise", "guide_license_number", "license_document", "license_expiry",
            "tourism_board_id", "is_verified", "years_of_experience", "certifications",
            "languages_certified", "previous_companies", "total_groups_led", "daily_rate",
            "custom_rates", "unavailable_dates", "accepts_group_bookings", "max_group_size",
            "accepts_last_minute", "last_minute_buffer_days", "linked_packages", "base_city",
            "base_country", "available_regions", "willing_to_travel", "max_travel_distance_km",
            "gallery_images", "rating", "review_tags", "notify_booking", "notify_reviews",
            "notify_cancellations", "enable_in_app_chat", "id_proof", "address_proof",
            "emergency_contact", "police_clearance", "is_available", "admin_notes",
            "force_availability_override", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class GuideProfileCompareSerializer(serializers.ModelSerializer):
    guide_name = serializers.CharField(source="user.name", read_only=True)
    price_per_day = serializers.DecimalField(source="daily_rate", max_digits=8, decimal_places=2, read_only=True)
    region_served = serializers.SerializerMethodField()
    experience_years = serializers.IntegerField(source="years_of_experience", read_only=True)
    affiliated_travel_company = serializers.CharField(source="travel_company", read_only=True)
    availability_status = serializers.BooleanField(source="is_available", read_only=True)

    class Meta:
        model = GuideProfile
        fields = [
            "id", "guide_name", "profile_photo", "price_per_day", "languages_spoken",
            "region_served", "experience_years", "is_verified", "specializations",
            "availability_status", "rating", "gallery_images", "affiliated_travel_company"
        ]

    def get_region_served(self, obj):
        return obj.region_expertise or []

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ["id", "user", "destination_name", "description", "package", "hotel", "guide", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "user", "message", "notification_type", "is_read", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

class UserOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOTP
        fields = ["id", "user", "otp", "is_verified", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class OTPVerifySerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user_id = attrs["user_id"]
        otp = attrs["otp"]
        otp_record = UserOTP.objects.filter(user_id=user_id, otp=otp, is_verified=False).first()
        if not otp_record:
            raise serializers.ValidationError("Invalid or expired OTP.")
        attrs["otp_record"] = otp_record
        return attrs

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, validators=[password_validator])

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[password_validator])

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user

class MostBookedGuideSerializer(serializers.ModelSerializer):
    guide_name = serializers.CharField(source="user.name", read_only=True)
    bookings_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = GuideProfile
        fields = [
            "id", "guide_name", "profile_photo", "guide_type", "base_city", "base_country",
            "rating", "is_verified", "is_available", "bookings_count"
        ]
        
class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = [
            "id",
            "language",
            "appearance",
            "currency",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]