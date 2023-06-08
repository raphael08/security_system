from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static
#redirecting to home page..
from django.views.generic import RedirectView

urlpatterns = [
    path('login_url/',include('uaa.urls')),
    path(' ',RedirectView.as_view(url='/login_url/')),
    
    path('fridgeAdmin/', admin.site.urls),
    path('',include('uaa.urls')),
    path('device/',include('fridge.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
    
# import execute