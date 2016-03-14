import os

from django.db import models
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo

from proyecto_boneo.apps.administracion.planes.models import Materia


def material_location(material, filename):
    return 'aula_virtual/biblioteca/material/{}-{}/{}'.format(material.materia.id,
                                                              material.materia.descripcion,
                                                              filename)


class BaseMaterial(models.Model):
    descripcion = models.CharField(max_length=100)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class Material(BaseMaterial):
    archivo = models.FileField(upload_to=material_location, null=True, blank=True)
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT)

    @property
    def nombre_archivo(self):
        return os.path.basename(self.archivo.name)

    def __str__(self):
        return self.descripcion


class SolicitudMaterial(BaseMaterial):
    motivo_rechazo = models.TextField(null=True, blank=True)
    aceptada = models.BooleanField(default=False)
    solicitante = models.ForeignKey(UsuarioBoneo, related_name='solicitante', default=None)
    material = models.ForeignKey(Material, null=True, blank=True, default=None)

    def __str__(self):
        return self.descripcion

# class MaterialAlumno(models.Model):
#     usuario = models.ForeignKey(UsuarioBoneo, related_name='materialpersonas')
#     material = models.ForeignKey(Material, related_name='materialpersonas')
#     marked_as_pinned = models.BooleanField()
