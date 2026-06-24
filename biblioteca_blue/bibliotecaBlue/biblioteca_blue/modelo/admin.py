from django.contrib import admin
from .models import Lector, Prestamo


@admin.register(Lector)
class LectorAdmin(admin.ModelAdmin):
    # Columnas que se mostrarán en la lista de lectores
    list_display = ('cedula', 'nombres', 'email')

    # Campos por los que podrás buscar en la barra de búsqueda
    search_fields = ('cedula', 'nombres', 'email')


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    # Columnas que se mostrarán en la lista de préstamos
    list_display = ('id_prestamo', 'lector', 'id_ejemplar', 'fecha_prestamo', 'fecha_estimada')

    # Filtros laterales para segmentar por fechas
    list_filter = ('fecha_prestamo', 'fecha_estimada')

    # Búsqueda (puedes buscar por el ID del ejemplar o datos del lector relacionado)
    search_fields = ('id_ejemplar', 'lector__cedula', 'lector__nombres')

