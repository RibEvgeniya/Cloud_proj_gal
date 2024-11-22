from django.conf.urls.static import static
from django.contrib import admin


from django.urls import path


from django.contrib import admin
from django.urls import path, include
import os

from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("gal.urls")),
    path("", include("photogallery.urls"))
    #path("acc",include("django.contrib.auth.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
