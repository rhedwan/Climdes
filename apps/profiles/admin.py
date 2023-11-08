from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "user", "gender", "phone_number", "country", "city"]
    list_display_links = ["pkid", "id", "user"]
    list_filter = [
        "pkid",
        "id",
    ]


class PhysicianPatientAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "physician", ]
    list_display_links = ["pkid", "id", "physician", ]
    list_filter = [
        "pkid",
        "id",
    ]


admin.site.register(Profile, ProfileAdmin)
