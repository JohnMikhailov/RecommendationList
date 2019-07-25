from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token, obtain_jwt_token

urlpatterns = [
    path('api/auth/', include('authentication.urls')),
    path('admin/', admin.site.urls)
]
