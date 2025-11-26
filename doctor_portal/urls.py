from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('appointment', views.appointments),
    path('prescription/',views.prescription)
]