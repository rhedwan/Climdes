from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from .models import Internship, Application

User = get_user_model()


class InternshipTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            password="testpassword",
            first_name="Test",
            last_name="User",
            email="test@example.com",
        )
        self.internship_data = {
            "title": "Test Internship",
            "description": "This is a test internship.",
            "location": "Test Location",
            "total_applicants": 10,
            "start_date": "2023-01-01T00:00:00Z",
            "end_date": "2023-01-31T23:59:59Z",
        }
        self.internship = Internship.objects.create(**self.internship_data)

    def test_internship_creation(self):
        self.assertEqual(Internship.objects.count(), 1)
        internship = Internship.objects.get(title="Test Internship")
        self.assertEqual(internship.location, "Test Location")

    def test_application_creation(self):
        application_data = {
            "applicant": self.user,
            "internship": self.internship,
            "status": Application.Status.SUBMITTED,
            "active": True,
        }
        application = Application.objects.create(**application_data)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(application.status, Application.Status.SUBMITTED)

    def test_internship_list_view(self):
        url = reverse("list_create_internship")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(response.data), Internship.objects.count())

    def test_application_list_create_view(self):
        url = reverse("apply_internship", kwargs={"internship_id": self.internship.id})
        self.client.force_login(self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Application.objects.count(), 0)

    def test_withdraw_application_view(self):
        application = Application.objects.create(
            applicant=self.user,
            internship=self.internship,
            status=Application.Status.SUBMITTED,
        )
        url = reverse("withdraw_internship", kwargs={"id": application.id})
        self.client.force_login(self.user)
        response = self.client.put(url, {"status": Application.Status.REJECTED})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        application.refresh_from_db()
        self.assertEqual(application.status, Application.Status.SUBMITTED)
