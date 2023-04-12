from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.index_view, name='index'),
    path('error/', views.error_view, name='error'),
    path('graphs/', views.graph_view, name='graphs'),
]