from django.conf.urls import url
from django.urls import path

from authentication import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('refresh/', views.refresh, name='refresh')
]
