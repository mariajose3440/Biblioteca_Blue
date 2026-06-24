from django.urls import path
from . import views

urlpatterns = [
    path('prestamo', views.guardar, name='guardar_prestamo'),
]
