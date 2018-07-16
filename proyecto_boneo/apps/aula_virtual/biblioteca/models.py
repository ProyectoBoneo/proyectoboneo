import os

from django.db import models
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo

from proyecto_boneo.apps.administracion.planes.models import Materia


def material_location(material, filename):
    return 'aula_virtual/biblioteca/material/{}-{}/{}'.format(material.materia.id,
                                                              material.materia.descripcion,
                                                              os.path.split(filename)[-1])


class BaseMaterial(models.Model):
    descripcion = models.CharField(max_length=100)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class MaterialManager(models.Manager):

    def publicados(self):
        queryset = super(MaterialManager, self).get_queryset()
        return queryset.filter(publicado=True)


class Material(BaseMaterial):
    objects = MaterialManager()

    archivo = models.FileField(upload_to=material_location, null=True, blank=True)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    publicado = models.BooleanField(null=False, default=True)

    @property
    def nombre_archivo(self):
        return os.path.basename(self.archivo.name)

    def __str__(self):
        return self.descripcion


class SolicitudMaterial(BaseMaterial):
    motivo_rechazo = models.TextField(null=True, blank=True)
    aceptada = models.BooleanField(default=False)
    pendiente_de_respuesta = models.BooleanField(default=True)
    solicitante = models.ForeignKey(UsuarioBoneo, related_name='solicitante', default=None, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, null=True, blank=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion
