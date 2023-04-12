from django.shortcuts import render
import matplotlib.pyplot as plt
import numpy as np
from vehicles.models import Vehicle

# Create your views here.
def index_view(request):
    return render(request, 'utils/index.html')

def error_view(request):
    return render(request, 'utils/error.html')


def graph_view(request):
    vehicles = Vehicle.objects.all()
    mpg_diffs = []

    for vehicle in vehicles:
        mpg_diffs.append(
            float(vehicle.combination_mpg_api) - float(vehicle.combination_mpg_predicted)
        )

    # Generate chart images using matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(range(len(mpg_diffs)), mpg_diffs)
    ax.set_xlabel("Vehicle Index")
    ax.set_ylabel("MPG Difference (API - Predicted)")
    fig.tight_layout()

    # Save chart images to a media folder
    chart_path = "utils/mpg_difference_chart.png"
    fig.savefig(chart_path)

    return render(
        request,
        "utils/graphs.html",
        {
            "vehicles": vehicles,
            "chart_path": chart_path,
        },
    )