from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


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





 
 
 
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_no = forms.CharField(max_length = 20)
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password1', 'password2']