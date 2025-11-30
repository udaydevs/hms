from django.urls import path
from . import views



app_name = "receptionistPortal"
urlpatterns = [
    path('appointments_data/', views.view_appointments),
    path('dashboard/', views.dashboard),
    path('update_appointment', views.update_appointments),
]