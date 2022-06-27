from django.urls import path
from index.views import home, document

urlpatterns = [
    path('', view=home, name='home'),
    path('<int:doc_id>/', view=document, name='document')
]
