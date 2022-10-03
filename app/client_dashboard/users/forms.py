from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser
from bootstrap_modal_forms.forms import BSModalModelForm



ROLE_CHOICES = (
    ("1", "Superuser"),
    ("2", "Admin"),
    ("4", "Editor"),
)


class CustomUserForm(forms.ModelForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'email',
            'role',
        ]


class CustomUserPassForm(forms.ModelForm):
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            'password1',
            'password2',
        ]


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'full_name')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'full_name')



class UserModelForm(BSModalModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email' , 'news_media', 'is_admin']