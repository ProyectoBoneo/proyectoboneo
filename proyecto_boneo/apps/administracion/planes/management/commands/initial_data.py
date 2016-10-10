import csv
import datetime
import json
import os
import random
import unidecode

from django.core.management import BaseCommand
from django.core.files import File

from proyecto_boneo.apps.administracion.alumnos.models import Alumno, Responsable, InscripcionAlumno
from proyecto_boneo.apps.administracion.personal.models import Profesor
from proyecto_boneo.apps.administracion.usuarios.models import UsuarioBoneo
from proyecto_boneo.apps.administracion.planes.models import Division, InstanciaCursado, Materia

from proyecto_boneo.apps.aula_virtual.clases.models import (ClaseVirtual, EjercicioVirtual,
                                                            RespuestaEjercicioVirtual, OpcionEjercicio,
                                                            ResultadoEvaluacion)

from proyecto_boneo.apps.aula_virtual.biblioteca.models import Material

from proyecto_boneo.apps.administracion.tutorias.models import EncuentroTutoria, Tutoria

BASE_DIR = os.path.dirname(__file__)


class Command(BaseCommand):
    help = 'This command populates the database with initial data'

    EMAIL_PROFESOR = 'profesor@boneo.com'
    EMAIL_ALUMNO = 'alumno@boneo.com'

    EJERCICIOS_POR_EVALUACION = 10
    OPCIONES_MULTIPLE_CHOICE = 3

    años_plan = range(1, 6)
    cantidad_divisiones = 4

    models = [
        Alumno,
        InscripcionAlumno,
        InstanciaCursado,
        Materia,
        Profesor,
        Responsable,
        UsuarioBoneo,
        ClaseVirtual,
        EjercicioVirtual,
        OpcionEjercicio,
        RespuestaEjercicioVirtual,
        ResultadoEvaluacion,
        Tutoria,
        EncuentroTutoria,
        Material
    ]

    def _get_random_person_data(self):
        nombre = random.choice(self.names)
        apellido = random.choice(self.last_names)
        return {
            'nombre': nombre,
            'apellido': apellido,
            'dni': random.randint(2*10**7, 4*10**7),
            'domicilio': '{} {}'.format(random.choice(self.street_names),
                                        random.randint(100, 3000)),
            'fecha_nacimiento': datetime.date.today() - datetime.timedelta(
                days=random.randint(10, 20) * 360),
            'email': '{}_{}@boneo.com'.format(nombre.lower(), apellido.lower())
        }

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

    def _create_usuario(self, email, is_alumno=False, is_profesor=False):
        usuario = UsuarioBoneo.objects.create(username=email, email=email)
        usuario.set_password("pass")
        usuario.is_alumno = is_alumno
        usuario.is_profesor = is_profesor
        usuario.save()
        return usuario

    def _create_responsable(self):
        responsable_data = self._get_random_person_data()
        email = responsable_data.pop('email')
        responsable_data['usuario'] = self._create_usuario(email)
        dni = responsable_data.pop('dni')
        responsable, _ = Responsable.objects.get_or_create(defaults=responsable_data, dni=dni)
        return responsable

    def _create_alumnos(self):
        divisiones = list(Division.objects.all())
        for i in range(0, 500):
            alumno_data = self._get_random_person_data()
            alumno_data['responsable'] = self._create_responsable()
            alumno_data['division'] = random.choice(divisiones)
            email = alumno_data.pop('email')
            dni = alumno_data.pop('dni')
            alumno_data['usuario'] = self._create_usuario(email, is_alumno=True)
            Alumno.objects.get_or_create(defaults=alumno_data, dni=dni)

    def _create_profesores(self):
        for i in range(0, 25):
            profesor_data = self._get_random_person_data()
            dni = profesor_data.pop('dni')
            email = profesor_data.pop('email')
            profesor_data['usuario'] = self._create_usuario(email, is_profesor=True)
            Profesor.objects.get_or_create(defaults=profesor_data, dni=dni)

    def _assign_profesores_materias(self):
        profesores = Profesor.objects.all()
        for instancia_cursado in InstanciaCursado.objects.all():
            instancia_cursado.profesor_titular = random.choice(profesores)
            instancia_cursado.save()

    def _create_inscripciones(self):
        for alumno in Alumno.objects.all():
            for instancia_cursado in alumno.division.instancias_cursado.all():
                InscripcionAlumno.objects.create(alumno=alumno,
                                                 instancia_cursado=instancia_cursado)

    def _create_test_users(self):
        UsuarioBoneo.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        self.alumno = Alumno(nombre='Juan', apellido='Pruebas', dni=36538548,
                             division=Division.objects.first(),
                             fecha_nacimiento=datetime.datetime.today() - datetime.timedelta(days=365*15),
                             responsable=self._create_responsable())
        self.alumno.crear_usuario(self.EMAIL_ALUMNO)
        self.alumno.save()
        self.profesor = Profesor(nombre='Alberto', apellido='Pruebas',
                                 dni=26538548,
                                 fecha_nacimiento=datetime.datetime.today() - datetime.timedelta(days=365*33))
        self.profesor.crear_usuario(self.EMAIL_PROFESOR)
        self.profesor.save()

    def _assign_test_users(self):
        for instancia_cursado in self.alumno.division.instancias_cursado.all():
            instancia_cursado.profesor_titular = self.profesor
            instancia_cursado.save()

    def _create_test_clases_virtuales(self):
        for idx, instancia_cursado in enumerate(self.alumno.division.instancias_cursado.all()):
            ejercicio_virtual = next((self.ejercicio_data[mat] for mat in self.ejercicio_data if
                                     mat == instancia_cursado.materia.descripcion.lower()), False)
            if ejercicio_virtual:
                if idx <= 2:
                    nombre = 'Evaluación {}'.format(instancia_cursado.materia.descripcion)
                    tipo = ClaseVirtual.EVALUACION
                else:
                    nombre = 'Clase {}'.format(instancia_cursado.materia.descripcion)
                    tipo = ClaseVirtual.CLASE_NORMAL

                clase_virtual = ClaseVirtual.objects.create(materia=instancia_cursado.materia,
                                                            tipo=tipo,
                                                            nombre=nombre)
                for ejercicio_data in ejercicio_virtual:

                    tipo_ejercicio = ejercicio_data['tipo']
                    ejercicio = EjercicioVirtual(tipo_ejercicio=tipo_ejercicio, puntaje=ejercicio_data['puntaje'],
                                                 clase_virtual=clase_virtual)
                    ejercicio.consigna = ejercicio_data['consigna']

                    ejercicio.save()

                    if tipo_ejercicio == EjercicioVirtual.MULTIPLE_CHOICE:
                        for opcion in ejercicio_data['opciones']:
                            OpcionEjercicio.objects.create(texto=opcion['texto'], opcion_correcta=opcion['opcion_correcta'],
                                                           ejercicio=ejercicio)

    def _create_tutorias(self):
        tutoria = Tutoria.objects.create(profesor=self.profesor, alumno=self.alumno, anio=2016)
        EncuentroTutoria.objects.create(tutoria=tutoria, fecha=datetime.date.today(), hora='16:00',
                                        resumen='Revisión de temas')

    def _create_materiales(self):
        base_material_path = os.path.join(BASE_DIR, 'data/materiales')
        material_files = {}
        for directory in os.listdir(base_material_path):
            if directory not in material_files:
                material_files[directory] = []
            for material_file in os.listdir(os.path.join(base_material_path, directory)):
                material_files[directory].append(os.path.join(base_material_path, directory, material_file))
        for idx, instancia_cursado in enumerate(self.alumno.division.instancias_cursado.all()):
            materia = unidecode.unidecode(instancia_cursado.materia.descripcion.lower())
            if materia in material_files:
                for material_file in material_files[materia]:
                    with open(material_file, mode='rb') as f:
                        Material.objects.create(materia=instancia_cursado.materia,
                                                descripcion='Material para {}'.format(materia),
                                                archivo=File(f))

    def _load_data(self):
        self.names = []
        self.last_names = []
        self.ejercicio_data = None

        with open(os.path.join(BASE_DIR, 'data/first_names.csv')) as names_file:
            names = csv.reader(names_file)
            for name in names:
                self.names.append(name[0])

        with open(os.path.join(BASE_DIR, 'data/last_names.csv')) as last_names_file:
            last_names = csv.reader(last_names_file)
            for last_name in last_names:
                self.last_names.append(last_name[0])

        self.street_names = []
        with open(os.path.join(BASE_DIR, 'data/street_names.csv')) as street_names:
            street_names = csv.reader(street_names)
            for street_name in street_names:
                self.street_names.append(street_name[0])

        with open(os.path.join(BASE_DIR, 'data/ejercicios.json')) as ejercicio_data:
            self.ejercicio_data = json.load(ejercicio_data)

    def handle(self, *args, **options):
        self.stdout.write('Cargando información inicial...')
        self._load_data()
        self.stdout.write('Limpiando estado actual...')
        self._clean_current_state()
        self.stdout.write('Creando materias...')
        self._create_materias()
        self.stdout.write('Creando divisiones...')
        self._create_divisiones()
        self.stdout.write('Creando instancias de cursado...')
        self._create_instancias_cursado()
        self.stdout.write('Creando profesores...')
        self._create_profesores()
        self.stdout.write('Creando alumnos...')
        self._create_alumnos()
        self.stdout.write('Asignando profesores a materias...')
        self._assign_profesores_materias()
        self.stdout.write('Creando usuarios de pruebas...')
        self._create_test_users()
        self.stdout.write('Creando inscripciones...')
        self._create_inscripciones()
        self.stdout.write('Asignando usuarios de pruebas...')
        self._assign_test_users()
        self.stdout.write('Creando clases virtuales...')
        self._create_test_clases_virtuales()
        self.stdout.write('Creando tutorías...')
        self._create_tutorias()
        self.stdout.write('Creando materiales...')
        self._create_materiales()
        self.stdout.write('Listo :)')
