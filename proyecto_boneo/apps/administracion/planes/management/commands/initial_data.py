from django.core.management import BaseCommand

from proyecto_boneo.apps.administracion.alumnos.models import Alumno, Responsable, InscripcionAlumno
from proyecto_boneo.apps.administracion.personal.models import Profesor
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo
from proyecto_boneo.apps.administracion.planes.models import Division, InstanciaCursado, Materia


class Command(BaseCommand):
    help = 'This command populates the database with initial data'

    años_plan = range(1, 6)
    cantidad_divisiones = 4

    models = [
        Alumno,
        InscripcionAlumno,
        InstanciaCursado,
        Materia,
        Profesor,
        Responsable,
        UsuarioBoneo
    ]

    def _bulk_create(self, klass, attributes_list):
        for instance in attributes_list:
            klass.objects.create(**instance)

    def _clean_current_state(self):
        for klass in self.models:
            klass.objects.all().delete()

    def _create_materias(self):
        materias = ['Lengua', 'Matemática', 'Ciencias Sociales', 'Formación Ética y Ciudadana',
                    'Ciencias Naturales', 'Educación Física', 'Música']
        attributes_list = []
        for materia in materias:
            for año in self.años_plan:
                attributes_list.append({'descripcion': materia, 'anio': año})
        self._bulk_create(Materia, attributes_list)

    def _create_divisiones(self):
        for año in self.años_plan:
            Division.objects.configurar_divisiones_año(año, self.cantidad_divisiones)

    def _create_instancias_cursado(self):
        InstanciaCursado.objects.generar_año_actual()

    def _create_alumnos(self):
        pass

    def _create_profesores(self):
        pass

    def _create_superuser(self):
        UsuarioBoneo.objects.create_superuser('boneo', 'boneo@admin.com', 'boneo')

    def handle(self, *args, **options):
        self.stdout.write('Limpiando estado actual...')
        self._clean_current_state()
        self.stdout.write('Creando materias de muestra...')
        self._create_materias()
        self.stdout.write('Creando divisiones de muestra...')
        self._create_divisiones()
        self.stdout.write('Creando instancias de cursado de muestra...')
        self._create_instancias_cursado()
        self.stdout.write('Creando super usuario boneo / boneo...')
        self._create_superuser()
        self.stdout.write('Listo :)')
