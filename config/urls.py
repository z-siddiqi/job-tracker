from django.contrib import admin
from django.urls import path, include

from boards.views import custom_handler404, custom_handler500

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('pages.urls')),
    path('boards/', include('boards.urls')),
]