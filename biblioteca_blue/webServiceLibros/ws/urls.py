from django.urls import path

from .views import (
    # Listados
    LibroListView,
    AutorListView,
    EditorialListView,
    EjemplarListView,
    GeneroLiterarioListView,
    # Detalle
    LibroDetailView,
    # Búsquedas
    BuscarLibroPorTituloView,
    BuscarLibroPorAutorView,
    BuscarLibroPorEditorialView,
    BuscarLibroPorGeneroView,
    BuscarLibroPorAnioView,
    BuscarAutorPorSeudonimoView,
    BuscarEditorialPorPaisView,
)

urlpatterns = [
    # ── Listas completas ──────────────────────────────────────────────
    path('libros/',          LibroListView.as_view(),          name='libros'),
    path('autores/',         AutorListView.as_view(),         name='autores'),
    path('editoriales/',     EditorialListView.as_view(),     name='editoriales'),
    path('ejemplares/',      EjemplarListView.as_view(),      name='ejemplares'),
    path('generos/',         GeneroLiterarioListView.as_view(), name='generos'),

    # ── Detalle de un libro (por ISBN) ──────────────────────────────
    path('libro/<str:isbn>/', LibroDetailView.as_view(), name='libro-detalle'),

    # ── Búsquedas ─────────────────────────────────────────────────────
    path('buscar/titulo/<str:titulo>/',          BuscarLibroPorTituloView.as_view(),      name='buscar-titulo'),
    path('buscar/autor/<str:seudonimo>/',        BuscarLibroPorAutorView.as_view(),       name='buscar-autor'),
    path('buscar/editorial/<str:nombre>/',       BuscarLibroPorEditorialView.as_view(),   name='buscar-editorial'),
    path('buscar/genero/<str:nombre_genero>/',   BuscarLibroPorGeneroView.as_view(),      name='buscar-genero'),
    path('buscar/anio/<str:anio>/',              BuscarLibroPorAnioView.as_view(),        name='buscar-anio'),

    # Búsquedas sobre otras entidades
    path('buscar/autor-por-seudonimo/<str:seudonimo>/', BuscarAutorPorSeudonimoView.as_view(), name='buscar-autor-seudonimo'),
    path('buscar/editorial-por-pais/<str:pais>/',       BuscarEditorialPorPaisView.as_view(),   name='buscar-editorial-pais'),
]