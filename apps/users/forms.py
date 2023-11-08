from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from dj_rest_auth.forms import AllAuthPasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from allauth.account.forms import default_token_generator
from allauth.account.adapter import get_adapter
from allauth.account.utils import user_pk_to_url_str

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email", "is_admin")

    error_messages = {
        "duplicate_email": "A user with this email already exists.",
    }

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages["duplicate_email"])


class CustomResetForm(AllAuthPasswordResetForm):
    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator", default_token_generator)

        for user in self.users:
            temp_key = token_generator.make_token(user)
            uid = user_pk_to_url_str(user)

            # custom url frontend

            url = f"https://communities.agnosyshealth.com/auth/reset-password?uid={uid}&token={temp_key}"

            context = {
                "current_site": current_site,
                "user": user,
                "password_reset_url": url,
                "request": request,
            }
            get_adapter(request).send_mail(
                "account/email/password_reset_key", email, context
            )
        return self.cleaned_data["email"]
