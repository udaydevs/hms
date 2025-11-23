from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('register', views.signUp),
    path('dropdowns/', views.dropDowns),
    path('login/', views.signIn),
    path('profile/', views.profile)
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)