# Actividad 2: Conexión a una base de datos PostgreSQL

* **Equipo:** Equipo 2. Biblioteca escolar
* **Integrantes:**
  * Jesús Francisco Arroyo Santos — `25VC0006`
  * Carlos Rubén Tolentino Romero — `25VC0024`
  * Aarón Ibarra Hernández — `25VC0178`

## Descripción
Aplicación web desarrollada en Python con Streamlit que se conecta de forma segura a una base de datos relacional en 
PostgreSQL para gestionar el catálogo de una biblioteca escolar. El proyecto implementa restricciones de integridad 
directamente en la base de datos y protege las credenciales mediante variables de entorno fuera del código fuente. 
Además, incluye manejo controlado de errores de conexión y consultas parametrizadas para prevenir inyección SQL.

## Requisitos
* Python 3.10 o superior
* PostgreSQL 14 o superior (con pgAdmin)

## Creación de la base de datos
1. Abre **pgAdmin 4** y conéctate al servidor local usando el usuario administrador (`postgres`).
2. Abre una herramienta de consulta (*Query Tool*) sobre la base `postgres` y ejecuta únicamente el **Paso 1** del 
archivo `crear_bd.sql` (`CREATE DATABASE biblioteca...`).
3. Actualiza la lista de bases de datos, selecciona la nueva base **`biblioteca`**, abre un nuevo *Query Tool* y ejecuta
el **Paso 2** completo de `crear_bd.sql` para crear la tabla `libros`, su índice, los 5 registros iniciales y el 
usuario `app_biblioteca`.

## .env
* Copia el archivo .env y cambia los datos solicitados si es necesario (especialmente la contraseña)

## Ejecución de la interfaz
* Abre la terminal y escribe:
* py -m streamlit run app_conexion.py

