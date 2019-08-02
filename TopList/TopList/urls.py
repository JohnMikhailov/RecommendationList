from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from TopList import settings

urlpatterns = [
    path('api/auth/', include('authentication.urls')),
    path('api/', include('user.urls')),
    path('api/', include('social.urls')),
    path('admin/', admin.site.urls)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
