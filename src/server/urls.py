from django.contrib import admin
from django.urls import path, include
import index.views as views

urlpatterns = [
    path('index/', include('index.urls')),
    path('admin/', admin.site.urls),
]