from .models import Internship, Application
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from .serializers import InternshipSerializer, ApplicationSerializer
from rest_framework import permissions, response
from django.shortcuts import get_object_or_404


class InternshipListCreateView(ListCreateAPIView):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    permission_classes = [permissions.IsAuthenticated]


class InternshipRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"


class InternshipApplicationListView(ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        internship = get_object_or_404(Internship, id=self.kwargs.get("internship_id"))
        return internship.internship_applications

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), many=True)

        return response.Response(serializer.data)


class ApplicationListCreateView(CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        internship = get_object_or_404(Internship, id=self.kwargs.get("internship_id"))
        serializer.save(applicant=user, internship=internship)


class WithdrawApplicationView(UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"
