from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm

from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(UserCreationForm):
    email = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    class Meta:
        model = User
        fields = ('email', 'password1')

class SignUpForm(UserCreationForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ('name', 'email', 'password1', 'password2', 'is_admin', 'is_instructor', 'is_student')

class PasswordReset(PasswordResetForm):
    email = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    
    class Meta:
        model = User
        fields = ('email',)


class CustomSetPasswordForm(SetPasswordForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    class Meta:
        model = User
        fields = ('password1', 'password2')