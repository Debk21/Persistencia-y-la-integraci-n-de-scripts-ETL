# Persistencia y automatización de procesos ETL

## Descripción

En este proyecto desarrollé un proceso ETL con Python y SQLite para extraer datos desde un archivo CSV, realizar una limpieza básica y guardarlos en una base de datos local.

El proceso calcula el importe total de cada venta a partir de la cantidad y el precio unitario. También permite volver a ejecutar la carga sin generar ventas duplicadas.

## Estructura del proyecto

* `datos/ventas.csv`: archivo de origen con los datos de ventas.
* `etl.py`: script principal que ejecuta el proceso ETL.
* `esquema.sql`: definición de la tabla de destino.
* `verificar.py`: script para comprobar la cantidad de registros y detectar duplicados.
* `requirements.txt`: dependencias del proyecto.
* `.gitignore`: archivos excluidos del repositorio.

La base de datos `ventas.db` se genera automáticamente al ejecutar el proceso.

## Requisitos

* Python 3 instalado.
* pip para instalar las dependencias.

## Pasos para ejecutar

1. Clonar el repositorio de GitHub o descargar sus archivos.

2. Abrir una terminal en la carpeta del proyecto.

3. Instalar las dependencias:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Ejecutar el proceso ETL:

   ```bash
   python etl.py
   ```

5. Comprobar los registros guardados:

   ```bash
   python verificar.py
   ```

## Persistencia y control de duplicados

La tabla `ventas` se define en `esquema.sql`. El campo `id_venta` funciona como clave primaria para identificar cada registro.

Durante la carga, el script utiliza `ON CONFLICT` para actualizar una venta existente cuando se encuentra el mismo identificador, en lugar de insertar otra fila con esa clave.

## Tecnologías utilizadas

* Python
* Pandas
* SQLite
* SQL
* Git y GitHub

## Pruebas realizadas

Se ejecutó el script ETL para comprobar la extracción, transformación y carga de los datos en SQLite.

La carga se ejecutó nuevamente para verificar que los identificadores existentes no generaran registros duplicados. También utilicé `verificar.py` para consultar la cantidad de ventas guardadas y detectar posibles duplicados.
