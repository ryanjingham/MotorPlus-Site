from django.shortcuts import render, redirect, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, VehicleForm
from .models import Vehicle, APIVehicle
from keras.models import load_model
import requests
import os
# Create your views here.


VEHICLES_API_KEY = 'ihU0CD4DEQgpa+OW+EsqHQ==n6COksm5iDFI1UhX'
VEHICLES_API_URL = f'https://api.api-ninjas.com/v1/cars?'

API_URL = 'localhost:3000/'
API_KEY = 'duffy'


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            print("invalid registration")
            print(form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    """
    Handle a user logging in to uweflix.
    
    If the request method is "POST", the function checks the provided username and password against the 
    database to authenticate the user. If the user is authenticated, the user is logged in and redirected 
    to the index page. If the user is not authenticated, an error message is displayed and the login form 
    is shown again. If the request method is not "POST", the login form is displayed.
    
    Returns:
        If the request method is "POST" and the user is not authenticated:
            The login form, with the error message passed in as context.
        If the request method is not "POST":
            The login form.
        Otherwise:
            A redirect to the index page.
    """
    
    # If the user has submitted the form
    if request.method == "POST":
        print("post")
        # Validate the form data
        username = request.POST.get('inputUsername')
        password = request.POST.get('inputPassword')
        user = authenticate(request, username=username, password=password)
        
        # If the user is authenticated
        if user is not None:
            login(request, user)
            return redirect('index')
        
        # If the user is not authenticated
        else:
            error_message = "Invalid username or password"
            context = {'error_message': error_message}
            print(error_message)
            return render(request, 'login.html', context)
    
    # If the user has not submitted the form
    else:
        print('get')
        # Display the login form
        return render(request, 'login.html')

def index_view(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def add_vehicle_view(request):
    if request.method == 'POST':
        make = request.POST.get('make')
        model = request.POST.get('model')
        year = request.POST.get('year')
        
        # API call to get the rest of the information
        url = VEHICLES_API_URL + f"limit=1&make={make}&model={model}&year={year}"
        response = requests.get(url, headers={'X-Api-Key': VEHICLES_API_KEY})
        data = response.json()
        
        # Extract the necessary information from the API response
        vehicle_class = data['class']
        fuel_type = data['fuel_type']
        transmission = data['transmission']
        city_mpg = data['city_mpg']
        highway_mpg = data['highway_mpg']
        displacement = data['displacement']
        cylinders = data['cylinders']
        combination_mpg = 0
        
        # Save the information to the database
        user = request.user
        vehicle = Vehicle.objects.create(
            user=user,
            make=make,
            model=model,
            year=year,
            class_ = vehicle_class,
            transmission = transmission,
            city_mpg = city_mpg,
            highway_mpg = highway_mpg,
            displacement = displacement,
            cylinders = cylinders,
            combination_mpg_api = combination_mpg
        )
        
        return redirect('vehicles')
    else:
        return render(request, 'create_vehicle.html')
    
def make_prediction_view(request, pk):
    user = request.user
    if user.is_authenticated():
        vehicle = Vehicle.objects.get(pk=pk)

        # Get the data for the vehicle
        data = {
            'make': vehicle.make,
            'model': vehicle.model,
            'year': vehicle.year,
            'class': vehicle.vehicle_class,
            'fuel_type': vehicle.fuel_type,
            'transmission': vehicle.transmission,
            'city_mpg': vehicle.city_mpg,
            'highway_mpg': vehicle.highway_mpg,
            'displacement': vehicle.displacement,
            'cylinders': vehicle.cylinders,
        }

        # Make the prediction
        headers = {'X-API-KEY': API_KEY}
        prediction = requests.post(API_URL + 'predict_keras', body={'input_data': data})

        # Save the prediction to the database
        vehicle.combination_mpg_predicted = prediction
        vehicle.save()

        # Redirect to the vehicle detail view
        return redirect('vehicle_details', pk=pk)