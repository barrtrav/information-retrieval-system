from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('index/', include('index.urls')),
    path('admin/', admin.site.urls),
]
