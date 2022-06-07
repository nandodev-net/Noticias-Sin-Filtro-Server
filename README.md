# Server noticias sin filtros

Scrapea noticias para alimentar el feed principal de la app de noticias sin filtros.

## Pre-requisitos 
1. Python 3.8 o superior.
2. Instalación de docker 

## Instalación 

1. Clonar este repo.
2. Crear y activar un virtual environment.
3. instalar dependencias básicas con `pip install -r requirements.txt`, lo que instalará poetry
4. Con `poetry` instalado, correr `poetry install` en la carpeta root del proyecto.

### Instalar el servidor localmente
En caso de que solo se deseen utilizar los servicios de django y postgres, es posible instalar el proyecto localmente. Para esto usamos los siguientes pasos:

1. Configurar la base de datos:   
    a. Logear a postgres usando `sudo -iu postgres psql`   
    b. correr los siguientes comandos:
```
CREATE DATABASE noticias_sin_filtro_dev;
CREATE USER vsf;
GRANT ALL PRIVILEGES ON DATABASE noticias_sin_filtro_dev TO vsf;
grant all privileges on databaSE noticias_sin_filtro_dev to vsf;
\q
```
2. Crear migraciones con:    
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
3. Crear super usuario con `python manage.py createsuperuser` y seguir los pasos para crear un super ususario con un nombre y contraseña de tu elección.
   
## Ejecución 
Existen 3 formas de correr el proyecto dependiendo de la cantidad de features activas que se desean tener en simultáneo.

* **En el host local:** Se utiliza la base de datos local y se ejecutan operaciones regulares de django. Se puede ejecutar `python manage.py runserver` para activar el servidor. Conveniente en casos donde queramos iterar localmente haciendo muchos cambios y sin probar servicios como los procesos asíncronos.  
  * Para esto también es conveniente activar el servidor de scraping en caso de que necesitamos probar el scraping, esto lo podemos hacer:    
     a. Abrimos una nueva terminal en la carpeta raíz del proyecto, activando el virtual environment donde estamos trabajando.    
     b. Cambia la carpeta `vsf_crawler`     
     c. Corremos el comando `scrapyd`. De esta forma, el servidor de scraping estará activo y las solicitudes que requieran el servicio de scraping funcionarán correctamente.    
* **Docker container de prueba:** Se utiliza la base de batos **transitoria** del servicio de bases de datos (postgres) que corre en docker, y tiene activo el servicio de scraping. Se puede usar ejecutando el script `run.sh` en la carpeta raíz del proyecto. 
* **Docker container de producción:** Se utiliza la base de datos **persistente** del servicio de base de datos de postgres que corre en el servidor. También soporta el servicio de tareas asíncronas y de nginx. Se puede ejecutar usando el script `run_prod.sh`

## Nota
Posiblemente necesites tener correctamente configurado los archivos environment correspondientes para cada estilo de ejecución:

1. **`.env.dev`** : Para el docker de prueba
2. **`.env.prod`** : Para el docker de producción
3. **`.env.prod.celery`** : para el docker de producción, y para la configuración de celery
4. **`.env.prod.db`** : para el docker de producción, y para la configuración de postgres
5. **`noticias_sin_filtro_server/.env`** : para la ejecución del proyecto localmente


