from django.db import models

from gutils.generic.datetime import calculate_age

from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo


class Persona(models.Model):
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    dni = models.BigIntegerField()
    domicilio = models.CharField(max_length=150)
    fecha_ingreso = models.DateField(auto_now_add=True)
    fecha_nacimiento = models.DateField()

    @property
    def edad(self):
        return calculate_age(self.fecha_nacimiento)

    @property
    def descripcion(self):
        return '{} {}'.format(self.nombre, self.apellido)

    def crear_usuario(self, email):
        self.usuario = UsuarioBoneo.objects.create(username=email, email=email)

    def __str__(self):
        return self.descripcion

    class Meta:
        abstract = True


class PersonaLegajo(Persona):
    legajo = models.BigIntegerField()

    @classmethod
    def _obtener_legajo(cls):
        try:
            legajo = cls.objects.latest('legajo').legajo + 1
        except cls.DoesNotExist:
            legajo = 1
        return legajo

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.pk and not self.legajo:
            self.legajo = self._obtener_legajo()
        super(PersonaLegajo, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True


class Profesor(PersonaLegajo):
    usuario = models.OneToOneField(UsuarioBoneo, related_name='profesor')

    def crear_usuario(self, email):
        super(Profesor, self).crear_usuario(self, email)
        self.usuario.is_profesor = True
