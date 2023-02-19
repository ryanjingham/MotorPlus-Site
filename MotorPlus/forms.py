from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Vehicle, User

class LoginForm(AuthenticationForm):
    pass

class VehicleFormSimple(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'transmission']

class VehicleFormFull(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'vehicle_class', 'fuel_type', 'transmission', 'city_mpg', 'highway_mpg', 'displacement', 'cylinders']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")    

