from django.urls import path
from .views import VistaPrincipal

urlpatterns = [
    path('', VistaPrincipal.as_view(), name="home"),
]