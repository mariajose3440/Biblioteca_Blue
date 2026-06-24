from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    Libro, Autor, Editorial, Ejemplar, GeneroLiterario,
    AutorLibro, LibroGeneroliterario
)
from .serializers import (
    LibroSerializer, AutorSerializer, EditorialSerializer,
    EjemplarSerializer, GeneroLiterarioSerializer,
    LibroDetailSerializer
)


# ── Listados ──────────────────────────────────────────────────────────
class LibroListView(generics.ListAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer


class AutorListView(generics.ListAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer


class EditorialListView(generics.ListAPIView):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializer


class EjemplarListView(generics.ListAPIView):
    queryset = Ejemplar.objects.all()
    serializer_class = EjemplarSerializer


class GeneroLiterarioListView(generics.ListAPIView):
    queryset = GeneroLiterario.objects.all()
    serializer_class = GeneroLiterarioSerializer


# ── Detalle (con información completa) ────────────────────────────────
class LibroDetailView(generics.RetrieveAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroDetailSerializer
    lookup_field = 'isbn'  # usamos ISBN como clave de búsqueda


# ── Búsquedas ──────────────────────────────────────────────────────────

class BuscarLibroPorTituloView(generics.ListAPIView):
    serializer_class = LibroSerializer

    def get_queryset(self):
        titulo = self.kwargs['titulo']
        return Libro.objects.filter(titulo__icontains=titulo)


class BuscarLibroPorAutorView(generics.ListAPIView):
    serializer_class = LibroSerializer

    def get_queryset(self):
        seudonimo = self.kwargs['seudonimo']
        # Obtenemos los autores que coinciden (puede haber varios con el mismo seudónimo)
        autores = Autor.objects.filter(seudonimo__icontains=seudonimo)
        # Buscamos los libros asociados a esos autores mediante AutorLibro
        libro_ids = AutorLibro.objects.filter(id_autor__in=autores).values_list('isbn_libro', flat=True)
        return Libro.objects.filter(isbn__in=libro_ids)


class BuscarLibroPorEditorialView(generics.ListAPIView):
    serializer_class = LibroSerializer

    def get_queryset(self):
        nombre = self.kwargs['nombre']
        editoriales = Editorial.objects.filter(nombre__icontains=nombre)
        return Libro.objects.filter(codigo_editorial__in=editoriales)


class BuscarLibroPorGeneroView(generics.ListAPIView):
    serializer_class = LibroSerializer

    def get_queryset(self):
        nombre_genero = self.kwargs['nombre_genero']
        generos = GeneroLiterario.objects.filter(nombre_genero__icontains=nombre_genero)
        libro_ids = LibroGeneroliterario.objects.filter(id_genero__in=generos).values_list('isbn_libro', flat=True)
        return Libro.objects.filter(isbn__in=libro_ids)


class BuscarLibroPorAnioView(generics.ListAPIView):
    serializer_class = LibroSerializer

    def get_queryset(self):
        anio = self.kwargs['anio']
        return Libro.objects.filter(anio_publicacion=anio)


class BuscarAutorPorSeudonimoView(generics.ListAPIView):
    serializer_class = AutorSerializer

    def get_queryset(self):
        seudonimo = self.kwargs['seudonimo']
        return Autor.objects.filter(seudonimo__icontains=seudonimo)


class BuscarEditorialPorPaisView(generics.ListAPIView):
    serializer_class = EditorialSerializer

    def get_queryset(self):
        pais = self.kwargs['pais']
        return Editorial.objects.filter(pais__icontains=pais)
