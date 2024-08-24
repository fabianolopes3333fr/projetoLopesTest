from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.devis , name='form_devis'),
    
]
