from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from .models import Profile, PhysicianPatient


class PhysicianReferralCodePhysician(serializers.ModelSerializer):
    class Meta:
        model = PhysicianPatient
        fields = ["referral_code"]


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    full_name = serializers.SerializerMethodField(read_only=True)
    profile_photo = serializers.SerializerMethodField()
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "full_name",
            "profile_photo",
            "country",
            "phone_number",
            "gender",
            "country",
            "city",
            "twitter_handle",
            "about_me",
        ]

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()

        return f"{first_name} {last_name}"

    def get_profile_photo(self, obj):
        return obj.profile_photo.url


class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    profile_photo_url = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = [
            "profile_photo",
            "profile_photo_url",
            "phone_number",
            "gender",
            "country",
            "city",
            "twitter_handle",
            "about_me",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("profile_photo")

        return representation
