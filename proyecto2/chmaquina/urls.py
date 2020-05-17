from django.urls import path
from .views import VistaPrincipal,vistaEjecucion,vistaMemoria,Salir

urlpatterns = [
    path('', VistaPrincipal.as_view(), name="home"),
    path('ejecucion/',vistaEjecucion.as_view(),name="ejecucion"),
    path('m/',vistaMemoria.as_view(),name="memoria"),
    path('s/',Salir.as_view(),name="salir")
]