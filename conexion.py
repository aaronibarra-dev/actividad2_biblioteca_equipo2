import os
import psycopg2
from dotenv import load_dotenv


def obtener_conexion():
    # Cargar las variables definidas en el archivo .env al entorno del sistema
    load_dotenv()

    # Leer valores opcionales aplicando valores por defecto si no existen
    servidor = os.getenv("DB_HOST") or "localhost"
    puerto_texto = os.getenv("DB_PORT") or "5432"

    # Verificar con un ciclo for que las variables obligatorias no estén vacías
    variables_obligatorias = ["DB_NAME", "DB_USER", "DB_PASSWORD"]
    variables_faltantes = []

    for nombre_variable in variables_obligatorias:
        valor_variable = os.getenv(nombre_variable)
        if valor_variable is None or valor_variable.strip() == "":
            variables_faltantes.append(nombre_variable)

    # Si falta al menos una variable obligatoria, lanzar ValueError con sus nombres
    if variables_faltantes:
        faltantes_texto = ", ".join(variables_faltantes)
        raise ValueError(f"Faltan variables en el archivo .env: {faltantes_texto}")

    # Obtener las credenciales ya validadas y convertir el puerto a entero
    base_datos = os.getenv("DB_NAME")
    usuario = os.getenv("DB_USER")
    contrasena = os.getenv("DB_PASSWORD")
    puerto = int(puerto_texto)

    # Establecer y retornar la conexión con un tiempo límite de 5 segundos
    return psycopg2.connect(
        host=servidor,
        port=puerto,
        dbname=base_datos,
        user=usuario,
        password=contrasena,
        connect_timeout=5,
    )


def consultar(sql, parametros=()):
    """Ejecuta una consulta SQL parametrizada y retorna columnas y filas."""
    # Inicializar conexión y cursor en None para garantizar cierre seguro en finally
    conexion = None
    cursor = None

    try:
        # Abrir conexión, crear el cursor y ejecutar la sentencia con parámetros
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)

        # Extraer nombres de columnas y recuperar todas las filas resultantes
        columnas = [descripcion[0] for descripcion in cursor.description] if cursor.description else []
        filas = cursor.fetchall()
        return columnas, filas

    finally:
        # Cerrar cursor y conexión siempre, incluso si ocurre una excepción
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()