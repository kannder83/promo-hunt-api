# WEB SCRAPING

Programa para obtener información de páginas web.

## Versiones:

- Revisar que cuente con una version reciente de python.

```bash
python3 --version
# Python 3.11.3
```

## Configurar entorno virtual:

- Crear el entorno virutal

```bash
python3 -m venv venv
```

- Ingresar al entorno virtual:

```bash
source venv/bin/activate
```

## Archivo .env

- Copiar el archivo "template.env" a ".env"

```bash
cp template.env .env
```

- Completar los datos del documento

```python
# API
MODE_PROD=False
DEBUG=True
VERSION="0.9.0"
DEV_URL="/"
PROD_URL="/"
ALLOWED_HOSTS=["*"]
WORKERS=1
PROD_PORT=8035
# DATABASE
DATABASE_HOSTNAME="mongodb"
DATABASE_PORT=27017
DATABASE_PASSWORD="Complex123*"
DATABASE_USERNAME="mongo"
DATABASE_WEB_USER="user"
DATABASE_WEB_PASSWORD="pass"
# EMAIL
EMAIL_SENDER="oneemail@gmail.com"
EMAIL_PASSWORD="s3cr3TPassWord987*!"
# PLAYWRIGHT
PLAYWRIGHT_HEADLESS=True
PLAYWRIGHT_SANDBOX=False
CHUNK_SIZE=1
TIMEOUT=6000
```

## Inicializar la aplicación:

- Tener instalado Docker
- Crear la imagen de Docker
- Iniciar el contenedor de Docker

## Funcionamiento de la aplicación:

A continuación de brinda el detalle para hacer uso de la aplicación.

### Creación de usuario

- Ingresar al endpoint, para crear el user_id se requiere el correo electrónico y un nombre.
- Al crear el usuario, se le asignará un user_id.

### Busqueda

- Realizar la búsqueda desde el endpoint correspondiente.
- Es necesario contar con el user_id para indicar el usuario que recibirá el correo electrónico.
- Esperar a que finalice el proceso de búsqueda en las tiendas.
- Al crear la búsqueda, recibirá un search_id que puede utilizar para hacer seguimiento del proceso hasta que el estado esté en "finished".
- Los resultados de la búsqueda se irán agregando al diccionario de la búsqueda.
- Una vez finalizado el proceso de búsqueda, se recibirá un correo electrónico.

### Realizar seguimiento

- En el endpoint de seguimiento se utilizará el search_id.
- Se debe indicar el precio o presupuesto para la búsqueda.
- El proceso se iniciará en segundo plano.
- Una vez finalizado el proceso de búsqueda, se enviará un correo electrónico.
- El diccionario de la búsqueda se actualizará con el valor del precio y la fecha/hora de la consulta.
- Se informará por correo electrónico acerca de los productos que estén por debajo del precio indicado al inicio.

## TODO:

- Crear CRUD para eliminar los productos que no se requiere seguimiento.
- Actualizar la documentación.
- Realizar tests unitarios.
- Realizar limpieza y borrar lo que no se necesita del programa.
