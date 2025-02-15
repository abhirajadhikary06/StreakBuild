from django import forms
from .models import FieldOfInterest, UploadedFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class FieldOfInterestForm(forms.Form):
    fields_of_interest = forms.ModelMultipleChoiceField(
        queryset=FieldOfInterest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['challenge', 'file']  # Use 'file' instead of 'image'