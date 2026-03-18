from django.contrib import admin

from .models import GuideProfile, Notification, User, UserOTP, UserProfile, Wishlist


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "user_type", "is_staff", "is_active", "created_at")
    search_fields = ("email", "name", "phone")
    list_filter = ("user_type", "is_staff", "is_active")


@admin.register(UserOTP)
class UserOTPAdmin(admin.ModelAdmin):
    list_display = ("user", "otp", "is_verified", "created_at")
    search_fields = ("user__email", "otp")
    list_filter = ("is_verified",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "profile_type", "kyc_status", "city", "country")
    search_fields = ("user__email", "user__name", "city", "country")
    list_filter = ("profile_type", "kyc_status", "theme")


@admin.register(GuideProfile)
class GuideProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "guide_type", "status", "is_verified", "is_available", "rating")
    search_fields = ("user__email", "user__name", "base_city", "base_country")
    list_filter = ("guide_type", "status", "is_verified", "is_available")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "destination_name", "hotel", "guide", "created_at")
    search_fields = ("user__email", "user__name", "destination_name")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "notification_type", "is_read", "created_at")
    search_fields = ("user__email", "user__name", "message")
    list_filter = ("notification_type", "is_read")
