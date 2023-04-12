from django import forms
from .models import Vehicle

class VehicleFormFull(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'transmission', 'displacement', 'cylinders', 'horsepower', 'weight', 'acceleration', 'origin']