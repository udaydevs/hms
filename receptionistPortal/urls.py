from django.urls import path
from . import views



app_name = "receptionistPortal"
urlpatterns = [
    path('appointments_data/', views.view_appointments)
    # path('SignIn/', views.SignIn),
    # path('SignOut/', views.SignOut),
]