from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Vehicle, User

class LoginForm(AuthenticationForm):
    pass

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")    

