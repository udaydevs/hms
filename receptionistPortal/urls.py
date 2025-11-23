from django.urls import path
from . import views



app_name = "receptionistPortal"
urlpatterns = [
    path('report/', views.report),
    # path('SignIn/', views.SignIn),
    # path('SignOut/', views.SignOut),
]