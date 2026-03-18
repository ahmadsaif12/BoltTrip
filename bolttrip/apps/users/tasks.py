from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email_task(subject, message, recipient_list, from_email=None):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email or getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=recipient_list,
        fail_silently=False,
    )


@shared_task
def send_otp_email_task(email, otp):
    subject = "Your BoltTrip OTP Code"
    message = f"Your verification code is {otp}."
    send_mail(
        subject=subject,
        message=message,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=[email],
        fail_silently=False,
    )
