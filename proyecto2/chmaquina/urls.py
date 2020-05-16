from django.urls import path
from .views import VistaPrincipal,vistaEjecucion,vistaMemoria

urlpatterns = [
    path('', vistaMemoria.as_view(), name="home"),
    path('ejecucion/',vistaEjecucion.as_view(),name="ejecucion"),
    path('m/',vistaMemoria.as_view(),name="memoria")
]