# serializers.py
from rest_framework import serializers
from .models import (
    Autor, Editorial, Ejemplar, GeneroLiterario, Libro,
    AutorLibro, LibroGeneroliterario, TelefonoEditorial
)


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'  # id (implícito) y seudononimo


class EditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = '__all__'  # codigo, nombre, pais


class GeneroLiterarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneroLiterario
        fields = '__all__'  # id_genero, nombre_genero


class LibroSerializer(serializers.ModelSerializer):
    # Para lectura, mostramos el objeto Editorial anidado
    codigo_editorial = EditorialSerializer(read_only=True)
    autores = serializers.SerializerMethodField()
    generos = serializers.SerializerMethodField()

    # Para escritura, permitimos enviar solo el ID de la editorial
    # Se debe definir un campo extra para escritura (opcional)
    # codigo_editorial_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Editorial.objects.all(), source='codigo_editorial', write_only=True
    # )

    class Meta:
        model = Libro
        fields = '__all__'

    def get_autores(self, obj):
        autores = Autor.objects.filter(autorlibro__isbn_libro=obj)
        return AutorSerializer(autores, many=True).data

    def get_generos(self, obj):
        generos = GeneroLiterario.objects.filter(librogeneroliterario__isbn_libro=obj)
        return GeneroLiterarioSerializer(generos, many=True).data


class EjemplarSerializer(serializers.ModelSerializer):
    isbn_libro = LibroSerializer(read_only=True)

    class Meta:
        model = Ejemplar
        fields = '__all__'  # id_ejemplar, isbn_libro


class AutorLibroSerializer(serializers.ModelSerializer):
    # Relaciones anidadas para lectura
    isbn_libro = LibroSerializer(read_only=True)
    id_autor = AutorSerializer(read_only=True)

    class Meta:
        model = AutorLibro
        fields = '__all__'  # isbn_libro, id_autor


class LibroGeneroliterarioSerializer(serializers.ModelSerializer):
    isbn_libro = LibroSerializer(read_only=True)
    id_genero = GeneroLiterarioSerializer(read_only=True)

    class Meta:
        model = LibroGeneroliterario
        fields = '__all__'  # isbn_libro, id_genero


class TelefonoEditorialSerializer(serializers.ModelSerializer):
    codigo_editorial = EditorialSerializer(read_only=True)

    class Meta:
        model = TelefonoEditorial
        fields = '__all__'  # codigo_editorial, telefono


# ------------------------------------------------------------
# Serializadores detallados con relaciones completas
# ------------------------------------------------------------

class LibroDetailSerializer(serializers.ModelSerializer):
    """
    Serializador que incluye toda la información relacionada:
    - Editorial (anidado)
    - Autores (lista de objetos Autor)
    - Géneros literarios (lista de objetos GeneroLiterario)
    - Ejemplares (lista de objetos Ejemplar)
    """
    codigo_editorial = EditorialSerializer(read_only=True)
    autores = serializers.SerializerMethodField()
    generos = serializers.SerializerMethodField()
    ejemplares = serializers.SerializerMethodField()

    class Meta:
        model = Libro
        fields = [
            'isbn', 'descripcion', 'anio_publicacion', 'titulo',
            'codigo_editorial', 'autores', 'generos', 'ejemplares'
        ]

    def get_autores(self, obj):
        # Obtener los autores a través de la tabla intermedia AutorLibro
        autor_libros = AutorLibro.objects.filter(isbn_libro=obj)
        autores = [al.id_autor for al in autor_libros]
        return AutorSerializer(autores, many=True).data

    def get_generos(self, obj):
        # Obtener los géneros a través de LibroGeneroliterario
        libro_generos = LibroGeneroliterario.objects.filter(isbn_libro=obj)
        generos = [lg.id_genero for lg in libro_generos]
        return GeneroLiterarioSerializer(generos, many=True).data

    def get_ejemplares(self, obj):
        ejemplares = Ejemplar.objects.filter(isbn_libro=obj)
        return EjemplarSerializer(ejemplares, many=True).data


class AutorDetailSerializer(serializers.ModelSerializer):
    """
    Serializador que muestra los libros escritos por el autor.
    """
    libros = serializers.SerializerMethodField()

    class Meta:
        model = Autor
        fields = ['id', 'seudononimo', 'libros']

    def get_libros(self, obj):
        autor_libros = AutorLibro.objects.filter(id_autor=obj)
        libros = [al.isbn_libro for al in autor_libros]
        return LibroSerializer(libros, many=True).data


class EditorialDetailSerializer(serializers.ModelSerializer):
    """
    Serializador que incluye los teléfonos y los libros de la editorial.
    """
    telefonos = serializers.SerializerMethodField()
    libros = serializers.SerializerMethodField()

    class Meta:
        model = Editorial
        fields = ['codigo', 'nombre', 'pais', 'telefonos', 'libros']

    def get_telefonos(self, obj):
        telefonos = TelefonoEditorial.objects.filter(codigo_editorial=obj)
        return TelefonoEditorialSerializer(telefonos, many=True).data

    def get_libros(self, obj):
        libros = Libro.objects.filter(codigo_editorial=obj)
        return LibroSerializer(libros, many=True).data