import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.settings import AUTH_USER_MODEL
from apps.profiles.models import Profile
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

User = get_user_model()


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        logger.info(f"{instance}'s profile has been created.")
        if instance.is_admin:
            logger.info(f"{instance}'s referral_code has been created.")
