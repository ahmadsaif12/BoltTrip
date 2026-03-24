from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import UserPreference


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_preference(sender, instance, created, **kwargs):
    if created:
        UserPreference.objects.get_or_create(user=instance)