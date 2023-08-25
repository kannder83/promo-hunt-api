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

```txt
DATABASE_HOSTNAME="localhost"
DATABASE_PORT=27017
DATABASE_PASSWORD="Complex123*"
DATABASE_USERNAME="mongo"
EMAIL_SENDER="oneemail@gmail.com"
EMAIL_PASSWORD="s3cVr3PassWord987*!"
```

## Comandos de la aplicación:

- Cargar el archivo con las URL y el ecommerce.

```bash
python3 upload_data.py
# Ingrese el nombre del archivo: data_files/url_format.csv
```

- Crear usuarios para enviar correo:

```bash
python3 create_user.py
# Ingrese el nombre: nombre
# Ingrese el email: nombre@xyz.co
```

- Correr el programa de web scraping.

```bash
python3 main.py
# PRODUCTS >> Se guardaron: 18 documentos.
```

## Instalar:

```bash
playwright install
```

## TODO:

- Crear endpoint para validar si ya finalizó el proceso de consulta.
- Enviar email al finalizar el proceso de consulta.
- Crear endpoint para visualiar usuarios.
- Crear un documento en la BD por cada busqueda que relacione el user_id para el envio de notificacion.
- Crear DRUD para eliminar los productos que no se requiere seguimiento.
- Crear umbral para comparar precio y notificación.
- Crear endpoint para activar el seguimiento de productos.
