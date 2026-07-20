from django.urls import path
from . import views
from django.shortcuts import render, redirect

urlpatterns = [
    path('prestamo', views.guardar, name='guardar_prestamo'),
    path('prestamo/<str:prestamo_id>/devolver', views.marcar_devuelto, name='marcar_devuelto'),
]
