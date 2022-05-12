from . import views
from django.urls import path
from .models import IndexDocument

try:
    import os
    db_name = os.environ['database']
    docs = IndexDocument.objects.using(db_name).all()
    urlsplus = [path(str(doc.id), views.viewdoc, name='str(doc.id)') for doc in docs]
except KeyError:
    urlsplus = []

urlpatterns = [
    path('', views.index, name='index'),
] + urlsplus