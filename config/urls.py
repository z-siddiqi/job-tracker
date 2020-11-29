from django.contrib import admin
from django.urls import path, include

from pages.views import custom_handler404, custom_handler500

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('nice-try/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('pages.urls')),
    path('boards/', include('boards.urls')),
    path('tasks/', include('tasks.urls')),
    path('notes/', include('notes.urls')),
]