from django.urls import path
from .views import (
    ProfileListAPIView,
    ProfileDetailAPIView,
    UpdateProfileAPIView,
    PhysicianPatientListAPIView,
    PhysicianReferralCodeView,
    PatientPhysicianListAPIView,
)

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="all-profiles"),
    path("me/", ProfileDetailAPIView.as_view(), name="my-profile"),
    path("update/", UpdateProfileAPIView.as_view(), name="update-profile"),
    path(
        "physician_patients/",
        PhysicianPatientListAPIView.as_view(),
        name="patients-profile",
    ),
    path(
        "patient_physician/",
        PatientPhysicianListAPIView.as_view(),
        name="physician-profile",
    ),
    path(
        "physician_referral_code/",
        PhysicianReferralCodeView.as_view(),
        name="referral_code",
    ),
]
