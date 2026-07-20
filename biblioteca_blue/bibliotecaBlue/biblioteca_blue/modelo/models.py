# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import mongoengine as me

class Lector(me.Document):
    cedula = me.StringField(max_length=10, required=True, unique=True)
    nombres = me.StringField(max_length=50, required=True)
    email = me.StringField(max_length=100, unique=True, sparse=True)

    meta = {'collection': 'lector'}

    def __str__(self):
        return self.nombres


class Prestamo(me.Document):
    lector = me.ReferenceField(Lector, required=True)
    id_ejemplar = me.StringField(max_length=10, required=True)
    fecha_prestamo = me.DateField(required=True)
    fecha_estimada = me.DateField()
    fecha_devolucion = me.DateField()

    meta = {'collection': 'prestamo'}

    def __str__(self):
        return f"Préstamo {self.id} - {self.lector.nombres}"
