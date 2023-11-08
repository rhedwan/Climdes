from django.db import models
from apps.common.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Internship(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    total_applicants = models.IntegerField(blank=True, null=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Application(TimeStampedModel):
    class Status(models.TextChoices):
        SUBMITTED = ("SUBMITTED", "SUBMITTED")
        PENDING = ("PENDING", "PENDING")
        REJECTED = ("REJECTED", "REJECTED")
        SUCCESS = ("SUCCESS", "SUCCESS")

    applicant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="applicant_applications"
    )
    internship = models.ForeignKey(
        Internship, on_delete=models.CASCADE, related_name="internship_applications"
    )
    status = models.CharField(
        choices=Status.choices, default=Status.SUBMITTED, max_length=50
    )
    active = models.BooleanField(default=True)
    submitted_on = models.DateTimeField(auto_now_add=True)
