# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Autor(models.Model):
    seudononimo = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'autor'


class AutorLibro(models.Model):
    isbn_libro = models.OneToOneField('Libro', models.DO_NOTHING, db_column='isbn_libro', primary_key=True)  # The composite primary key (isbn_libro, id_autor) found, that is not supported. The first column is selected.
    id_autor = models.ForeignKey(Autor, models.DO_NOTHING, db_column='id_autor')

    class Meta:
        managed = False
        db_table = 'autor_libro'
        unique_together = (('isbn_libro', 'id_autor'),)

class Editorial(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25)
    pais = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'editorial'


class Ejemplar(models.Model):
    id_ejemplar = models.AutoField(primary_key=True)
    isbn_libro = models.ForeignKey('Libro', models.DO_NOTHING, db_column='isbn_libro', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ejemplar'


class GeneroLiterario(models.Model):
    id_genero = models.AutoField(primary_key=True)
    nombre_genero = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'genero_literario'


class Libro(models.Model):
    isbn = models.CharField(primary_key=True, max_length=15)
    descripcion = models.TextField(blank=True, null=True)
    anio_publicacion = models.CharField(max_length=4, blank=True, null=True)
    titulo = models.CharField(max_length=25)
    codigo_editorial = models.ForeignKey(Editorial, models.DO_NOTHING, db_column='codigo_editorial')

    class Meta:
        managed = False
        db_table = 'libro'


class LibroGeneroliterario(models.Model):
    isbn_libro = models.OneToOneField(Libro, models.DO_NOTHING, db_column='isbn_libro', primary_key=True)  # The composite primary key (isbn_libro, id_genero) found, that is not supported. The first column is selected.
    id_genero = models.ForeignKey(GeneroLiterario, models.DO_NOTHING, db_column='id_genero')

    class Meta:
        managed = False
        db_table = 'libro_generoliterario'
        unique_together = (('isbn_libro', 'id_genero'),)


class TelefonoEditorial(models.Model):
    codigo_editorial = models.OneToOneField(Editorial, models.DO_NOTHING, db_column='codigo_editorial', primary_key=True)  # The composite primary key (codigo_editorial, telefono) found, that is not supported. The first column is selected.
    telefono = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'telefono_editorial'
        unique_together = (('codigo_editorial', 'telefono'),)
