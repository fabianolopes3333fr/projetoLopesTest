from django.urls import path
from . import views

urlpatterns = [
    path('timeout/',  views.timeout_view, name='timeout'),
]
