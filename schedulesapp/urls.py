# schedulesapp/urls.py
from django.urls import path
from .views import schedule_view,register_user  # Import your view function

urlpatterns = [
    path('schedules/', schedule_view, name='schedules'),  # Ensure this matches the name used in the template
    path('schedules/', register_user, name='register_user'),  # For the registration form
  
]
