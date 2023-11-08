from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from apps.common.models import TimeStampedModel
import uuid
import environ

env = environ.Env()
User = get_user_model()


class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = (
            "M",
            _("Male"),
        )
        FEMALE = (
            "F",
            _("Female"),
        )
        OTHERS = (
            "O",
            _("OTHERS"),
        )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), max_length=30, default="+2348123456789"
    )
    about_me = models.TextField(
        verbose_name=_("About Me"), default="say something about yourself"
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=20,
        choices=Gender.choices,
        default=Gender.OTHERS,
    )
    country = CountryField(
        verbose_name=_("Country"), default="NG", blank=False, null=False
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=180,
        default="Lagos",
        blank=False,
        null=False,
    )
    profile_photo = models.ImageField(blank=True, null=True)
    twitter_handle = models.CharField(
        verbose_name=_("Twitter Handle"), max_length=20, blank=True
    )
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", blank=True
    )

    def __str__(self) -> str:
        return f"{self.user.first_name}'s Profile"




