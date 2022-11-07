from django.urls import path
from . import views

app_name = 'report_tool'

urlpatterns = [
    path('', views.report_cleaner),
]
