from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

@shared_task
def send_email_task(subject, message, recipient_list, from_email=None, html_message=None):
    """
    Generic email sender task.
    Supports optional HTML content.
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email or getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=recipient_list,
        fail_silently=False,
        html_message=html_message
    )

@shared_task
def send_otp_email_task(email, otp):
    subject = "BoltTrip Verification Code"
    message = f"Hello! Your verification code is: {otp}. It will expire in 10 minutes."
    html_message = f"""
<html>
<body>
<p>Hello!</p>
<p>Your verification code is: <strong>{otp}</strong></p>
<p>It will expire in 10 minutes.</p>
</body>
</html>
"""
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
        html_message=html_message
    )