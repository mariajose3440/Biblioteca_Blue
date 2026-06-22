from django.contrib import admin

# Register your models here.

from .models import (
    Lector,
    Prestamo,
)


# ─── Inline: Préstamos dentro de Lector ───────────────────────────────────────
class PrestamoInline(admin.TabularInline):
    model = Prestamo
    extra = 1
    fields = ("isbn", "fecha_prestamo", "fecha_estimada")
    verbose_name = "Préstamo"
    verbose_name_plural = "Historial de Préstamos"


# ─── Lector ───────────────────────────────────────────────────────────────────
@admin.register(Lector)
class LectorAdmin(admin.ModelAdmin):
    list_display = ("id", "cedula", "nombres", "email")
    list_filter = ("nombres",)
    search_fields = ("cedula", "nombres", "email")
    ordering = ("nombres",)
    inlines = [PrestamoInline]

    fieldsets = (
        ("Datos de Identificación", {
            "fields": ("cedula",)
        }),
        ("Información del Lector", {
            "fields": ("nombres", "email")
        }),
    )


# ─── Préstamo ─────────────────────────────────────────────────────────────────
@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = (
        "id_prestamo",
        "lector",
        "isbn",
        "fecha_prestamo",
        "fecha_estimada",
    )
    list_filter = ("fecha_prestamo", "fecha_estimada")
    search_fields = (
        "id_prestamo",
        "isbn",
        "lector__nombres",
        "lector__cedula",
    )
    ordering = ("-fecha_prestamo",)
    autocomplete_fields = ("lector",)

    fieldsets = (
        ("Información del Préstamo", {
            "fields": ("lector", "isbn")
        }),
        ("Fechas de Control", {
            "fields": ("fecha_prestamo", "fecha_estimada")
        }),
    )