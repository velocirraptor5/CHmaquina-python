from django.urls import path
from .views import VistaPrincipal
from .views import vistaEjecucion

urlpatterns = [
    path('', VistaPrincipal.as_view(), name="home"),
    path('ejecucion/',vistaEjecucion.as_view(),name="ejecucion")
]