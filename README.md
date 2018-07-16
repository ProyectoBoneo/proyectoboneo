#Proyecto boneo

##Instrucciones para desarrollo:

1. Clonar el repositorio
    ```
    git clone git@github.com:ProyectoBoneo/proyectoboneo
    ```
2. Crear un virtualenv
    ```
    mkvirtualenv boneo
    echo "cd '~/projects/proyectofinalcode/proyecto_boneo'" >> ~/.virtualenvs/boneo/bin/post_activate
    ```
3. Instalar las dependencias
    ```
    workon boneo
    pip install -r requirements.txt
    ```
4. Crear base de datos
Crear base de datos PostgreSQL, llamada `proyecto_boneo`, cuyo owner es `boneo` / `boneo`
5. Correr migraciones
    ```
    python manage.py migrate
    ```    
    
6. Carga de datos iniciales
Este paso cargará los datos iniciales de prueba del sistema y creará el superuser `boneo` / `boneo`
    ```
    python manage.py initial_data
    ```
7. Correr el servidor
    ```
    python manage.py runserver
    ```
