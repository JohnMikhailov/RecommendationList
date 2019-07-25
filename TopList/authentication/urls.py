from django.conf.urls import url
from django.urls import path

from authentication import views

urlpatterns = [
    url('login/', views.login, name='login'),
    url('registration/', views.registration, name='registration'),
    url('refresh/', views.refresh, name='refresh')
]
