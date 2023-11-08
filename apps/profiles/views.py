from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import Profile, PhysicianPatient
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import (
    ProfileSerializer,
    UpdateProfileSerializer,
    PhysicianReferralCodePhysician,
)
from apps.profiles.serializers import ProfileSerializer
from rest_framework.exceptions import PermissionDenied
from apps.users.serializers import UserSerializer
import cloudinary


class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination
    renderer_classes = [ProfilesJSONRenderer]


class ProfileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    renderer_classes = [ProfileJSONRenderer]

    def get_queryset(self):
        queryset = Profile.objects.select_related("user")
        return queryset

    def get_object(self):
        user = self.request.user
        profile = self.get_queryset().get(user=user)
        return profile


class UpdateProfileAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfileSerializer
    renderer_classes = [ProfileJSONRenderer]
    parser_classes = (MultiPartParser,)

    def get_object(self):
        profile = self.request.user.profile
        return profile

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if "profile_photo" in self.request.FILES:
            if instance.profile_photo:
                public_id = instance.profile_photo.url.split("/")[-1].split(".")[0]
                cloudinary.uploader.destroy(public_id, invalidate=True)

            uploaded_image = cloudinary.uploader.upload(
                self.request.FILES["profile_photo"]
            )
            instance.profile_photo = uploaded_image["url"]
            instance.save()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PhysicianPatientListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        profile = self.request.user.profile
        return profile

    def get(self, request, *args, **kwargs):
        try:
            patients = PhysicianPatient.objects.get(
                physician=self.get_object()
            ).patients.all()
            serializer = self.get_serializer(patients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PhysicianPatient.DoesNotExist:
            raise PermissionDenied()


class PhysicianReferralCodeView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PhysicianPatient.objects.all()
    serializer_class = PhysicianReferralCodePhysician

    def get_object(self):
        profile = self.request.user.profile
        return profile

    def get(self, request, *args, **kwargs):
        try:
            physician = PhysicianPatient.objects.get(physician=self.get_object())
            serializer = self.get_serializer(physician)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PhysicianPatient.DoesNotExist:
            raise PermissionDenied()


class PatientPhysicianListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        user = self.request.user
        return user

    def get(self, request, *args, **kwargs):
        try:
            patient_physician = PhysicianPatient.objects.get(patients=self.get_object())
            physician_profile = patient_physician.physician
            serializer = self.get_serializer(physician_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PhysicianPatient.DoesNotExist:
            return Response({}, status=status.HTTP_200_OK)
