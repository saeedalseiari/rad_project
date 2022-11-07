from django.urls import path
from . import views

urlpatterns = [
    path('', views.tirads, name='thyroid-page'),
    path('home', views.home),
]
