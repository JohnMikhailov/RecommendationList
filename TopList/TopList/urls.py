from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token, obtain_jwt_token

from TopList import settings

urlpatterns = [
    path('api/auth/', include('authentication.urls')),
    path('api/', include('user.urls')),
    path('admin/', admin.site.urls)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
