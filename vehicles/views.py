from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import VehicleFormFull
from .models import Vehicle, APIVehicle
import requests
import os
import logging

# Create your views here.

VEHICLES_API_KEY = 'ihU0CD4DEQgpa+OW+EsqHQ==n6COksm5iDFI1UhX'
VEHICLES_API_URL = f'https://api.api-ninjas.com/v1/cars?'

API_URL = 'http://localhost:5000/'
API_KEY = 'duffy'

logger = logging.getLogger(__name__)

    
def add_vehicle_full(request):
    if request.method == 'POST':
        form = VehicleFormFull(request.POST)
        if form.is_valid():
            make = form.cleaned_data['make']
            model = form.cleaned_data['model']
            year = form.cleaned_data['year']    
            transmission = form.cleaned_data['transmission']
            displacement = form.cleaned_data['displacement']
            cylinders = form.cleaned_data['cylinders']
            horsepower = form.cleaned_data['horsepower']
            weight = form.cleaned_data['weight']
            acceleration = form.cleaned_data['acceleration']
            origin = form.cleaned_data['origin']

            user = request.user
            vehicle = Vehicle.objects.create(
                user=user,
                make=make,
                model=model,
                year=year,
                transmission=transmission,
                displacement=displacement,
                cylinders=cylinders,
                horsepower=horsepower,
                weight=weight,
                acceleration=acceleration,
                origin=origin,
                mpg_api=0,
                mpg_predicted=0
            )
            
            return redirect('index')
        else:
            logger.error(form.errors)
            
    form = VehicleFormFull()
    context = {'form': form}
    return render(request, 'vehicles/add_vehicle_full.html', context)

def make_prediction_view(request, pk):
    if request.user.is_authenticated:
        vehicle = Vehicle.objects.get(pk=pk)

        # Convert origin and year to classifier input format
        origin_dict = {'USA': '1', 'Europe': '2', 'Japan': '3'}
        year = str(vehicle.year)[-2:]
        # convert to lbs
        weight = vehicle.weight *2.205

        # Get the data for the vehicle in classifier input format
        data = {
            'cylinders': vehicle.cylinders,
            'displacement': vehicle.displacement,
            'horsepower': vehicle.horsepower,
            'weight': weight,
            'acceleration': vehicle.acceleration,
            'year': year,
            'origin': origin_dict[vehicle.origin],
        }

        # Make the prediction
        headers = {'X-API-KEY': API_KEY}
        try:
            # Send a POST request to the API to make a prediction
            prediction = requests.post(API_URL + 'predict_keras', json={'input_data': data}, headers=headers)
            prediction = prediction.json()['prediction']

            # Update the vehicle object with the prediction
            vehicle.mpg_predicted = prediction
            vehicle.save()

            # Log the prediction
            logging.info(f"Prediction for vehicle {vehicle.pk}: {prediction}")
        except Exception as e:
            # Handle the exception
            logging.error(f"Error making prediction for vehicle {vehicle.pk}: {e}")
            logging.error(f"JSON Response: {prediction.text}")
            return render(request, 'vehicles/view_vehicle_details.html', {'vehicle': vehicle, 'error': e})

    return render(request, 'vehicles/view_vehicle_details.html', {'vehicle': vehicle})

    
def vehicle_details_view(request, pk):
    vehicle = Vehicle.objects.get(pk=pk)
    return render(request, 'vehicles/view_vehicle_details.html', {'vehicle': vehicle})

@login_required(login_url='/login')
def view_vehicles_view(request):
    vehicles = Vehicle.objects.filter(user=request.user)
    return render(request, 'vehicles/view_vehicles.html', {'vehicles': vehicles})