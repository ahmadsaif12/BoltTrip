from django.contrib import admin
from .models import Booking, BookingPayment, BookingTraveler


class BookingTravelerInline(admin.TabularInline):
    model = BookingTraveler
    extra = 0


class BookingPaymentInline(admin.TabularInline):
    model = BookingPayment
    extra = 0


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "booking_reference",
        "user",
        "booking_type",
        "booking_status",
        "payment_status",
        "start_date",
        "total_amount",
        "currency",
    )
    search_fields = ("booking_reference", "user__email", "contact_name", "contact_email")
    list_filter = ("booking_type", "booking_status", "payment_status", "currency")
    inlines = [BookingTravelerInline, BookingPaymentInline]


@admin.register(BookingTraveler)
class BookingTravelerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "booking", "nationality")
    search_fields = ("full_name", "booking__booking_reference")


@admin.register(BookingPayment)
class BookingPaymentAdmin(admin.ModelAdmin):
    list_display = ("booking", "payment_method", "amount", "payment_status", "paid_at")
    search_fields = ("booking__booking_reference", "transaction_id")
    list_filter = ("payment_status", "payment_method", "currency")
