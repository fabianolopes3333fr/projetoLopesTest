from django.urls import path # type: ignore
from perfil.views import perfil_view

urlpatterns = [
    path('<int:id>/', perfil_view, name='perfil'),
]