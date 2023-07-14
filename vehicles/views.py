from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import VehicleFormFull
from .models import Vehicle, APIVehicle
import requests
import os
import logging

# Create your views here.

VEHICLES_API_KEY = "ihU0CD4DEQgpa+OW+EsqHQ==n6COksm5iDFI1UhX"
VEHICLES_API_URL = f"https://api.api-ninjas.com/v1/cars?"

API_URL = "http://localhost:5000/"
API_KEY = "duffy"

logger = logging.getLogger(__name__)


def add_vehicle_full(request):
    if request.method == "POST":
        form = VehicleFormFull(request.POST)
        if form.is_valid():
            make = form.cleaned_data["make"]
            model = form.cleaned_data["model"]
            year = form.cleaned_data["year"]
            transmission = form.cleaned_data["transmission"]

            # Make a request to the API to get the cylinders and displacement
            params = {
                "make": make,
                "model": model,
                "year": year,
                "transmission": transmission,
            }
            headers = {"X-Api-Key": VEHICLES_API_KEY}
            response = requests.get(VEHICLES_API_URL, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                if data:
                    vehicle_data = data[0]
                    cylinders = vehicle_data["cylinders"]
                    displacement = vehicle_data["displacement"]
                    mpg_api = vehicle_data["combination_mpg"]
                else:
                    # Handle the case where the API request was successful but did not find a matching vehicle
                    return HttpResponseBadRequest("Vehicle not found")
            else:
                # Handle the case where the API request failed
                return HttpResponseBadRequest("Error accessing API")

            horsepower = form.cleaned_data["horsepower"]
            weight = form.cleaned_data["weight"]
            acceleration = form.cleaned_data["acceleration"]
            origin = form.cleaned_data["origin"]

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
                mpg_predicted=0,
            )

            return redirect("index")
        else:
            logger.error(form.errors)

    form = VehicleFormFull()
    context = {"form": form}
    return render(request, "vehicles/add_vehicle_full.html", context)


def make_prediction_view(request, pk):
    if request.user.is_authenticated:
        vehicle = Vehicle.objects.get(pk=pk)

        year = str(vehicle.year)[-2:]
        # convert to lbs
        weight = vehicle.weight * 2.205

        # Get the data for the vehicle in classifier input format
        data = {
            "cylinders": vehicle.cylinders,
            "displacement": vehicle.displacement,
            "horsepower": vehicle.horsepower,
            "weight": weight,
            "acceleration": vehicle.acceleration,
            "year": year,
        }

        # Make the prediction

        headers = {"X-API-Key": request.user.API_KEY}
        try:
            # Send a POST request to the API to make a prediction
            response = requests.post(
                API_URL + "predict_mpg", json={"input_data": data}, headers=headers
            )
            prediction_response = response.json()
            prediction_val = prediction_response["prediction"]
            print(prediction_val)
            # Update the vehicle object with the prediction
            vehicle.mpg_predicted = prediction_val
            vehicle.save()

            # Log the prediction
            logging.info(f"Prediction for vehicle {vehicle.pk}: {response}")
        except ConnectionError as e:
            # Handle the connection error
            logging.error(f"Error connecting to API: {e}")
            return render(
                request,
                "vehicles/view_vehicle_details.html",
                {"vehicle": vehicle, "error": "Error connecting to API"},
            )
        except Exception as e:
            # Handle any other exceptions
            logging.error(f"Error making prediction for vehicle {vehicle.pk}: {e}")
            logging.error(f"JSON Response: {response.text}")
            return render(
                request,
                "vehicles/view_vehicle_details.html",
                {"vehicle": vehicle, "error": e},
            )

    return render(request, "vehicles/view_vehicle_details.html", {"vehicle": vehicle})


def vehicle_details_view(request, pk):
    vehicle = Vehicle.objects.get(pk=pk)
    return render(request, "vehicles/view_vehicle_details.html", {"vehicle": vehicle})


@login_required(login_url="/login")
def view_vehicles_view(request):
    vehicles = Vehicle.objects.filter(user=request.user)
    return render(request, "vehicles/view_vehicles.html", {"vehicles": vehicles})
