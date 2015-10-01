import os

from django.db import models

from proyecto_boneo.apps.administracion.planes.models import Materia


def material_location(material, filename):
    return 'aula_virtual/biblioteca/material/{}-{}/{}'.format(material.materia.id,
                                                              material.materia.descripcion,
                                                              filename)


class Material(models.Model):
    descripcion = models.CharField(max_length=100)
    observaciones = models.TextField(null=True, blank=True)
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT)
    archivo = models.FileField(upload_to=material_location, null=True, blank=True)

    @property
    def nombre_archivo(self):
        return os.path.basename(self.archivo.name)

    def __str__(self):
        return self.descripcion
