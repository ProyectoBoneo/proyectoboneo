import os

import firebase_admin

from django.apps import AppConfig
from firebase_admin import credentials

AUTH_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'firebase_auth',
                         'proyectoboneoapp-firebase-adminsdk-45lrh-6e9bc587a4.json')


class FirebaseConfig(AppConfig):
    name = 'proyecto_boneo.apps.firebase'

    def ready(self):
        certificate = credentials.Certificate(AUTH_FILE)
        firebase_admin.initialize_app(certificate)
