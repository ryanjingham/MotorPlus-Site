from django.urls import path
from . import views

urlpatterns = [
    path('add_vehicle_full', views.add_vehicle_full, name='add_vehicle_full'),
    path('view_vehicles/', views.view_vehicles_view, name='view_vehicles'),
    path('vehicle_details/<int:pk>', views.vehicle_details_view, name='vehicle_details'),
    path('vehicle_details/<int:pk>/make_prediction', views.make_prediction_view, name='make_prediction'),
]