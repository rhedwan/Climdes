from rest_framework import serializers
from .models import Internship, Application
from apps.users.serializers import UserSerializer
class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = "__all__"


class ApplicationSerializer(serializers.ModelSerializer):
    # internship = InternshipSerializer(read_only=True)
    # applicant = UserSerializer(read_only=True)
    class Meta:
        model = Application
        # fields = "__all__"
        exclude = ["internship", "applicant"]