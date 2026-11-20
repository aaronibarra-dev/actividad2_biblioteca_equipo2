import os
import psycopg2
import streamlit as st
from dotenv import load_dotenv
from conexion import consultar

# Configuración inicial de la página de Streamlit
st.set_page_config(page_title="Biblioteca Escolar - PostgreSQL", layout="wide")

# Título del escenario y subtítulo con el nombre del equipo
st.title("Biblioteca Escolar - Conexión a PostgreSQL")
st.caption("Equipo 2. Biblioteca escolar")

# Cargar variables de entorno únicamente para mostrar los datos de conexión
load_dotenv()
servidor_actual = os.getenv("DB_HOST") or "localhost"
puerto_actual = os.getenv("DB_PORT") or "5432"
base_actual = os.getenv("DB_NAME") or "No definida"
usuario_actual = os.getenv("DB_USER") or "No definido"
clave_actual = os.getenv("DB_PASSWORD") or ""
clave_oculta = "*" * len(clave_actual) if clave_actual else "No definida"

# Sección 1: Datos de conexión configurados en .env
st.subheader("Datos de conexión")
col_d1, col_d2, col_d3, col_d4, col_d5 = st.columns(5)
col_d1.write(f"**Servidor:** `{servidor_actual}`")
col_d2.write(f"**Puerto:** `{puerto_actual}`")
col_d3.write(f"**Base de datos:** `{base_actual}`")
col_d4.write(f"**Usuario:** `{usuario_actual}`")
col_d5.write(f"**Contraseña:** `{clave_oculta}`")

# Botón para probar la conexión directamente contra PostgreSQL
if st.button("Probar conexión"):
    try:
        _, info_servidor = consultar("SELECT current_database(), current_user, version();")
        bd_conectada, usuario_conectado, version_pg = info_servidor[0]
        st.success(
            f"Conexión exitosa | Base de datos: **{bd_conectada}** | "
            f"Usuario: **{usuario_conectado}** | Versión: {version_pg}"
        )
    except ValueError as error_val:
        st.error(f"Error de configuración: {error_val}")
    except psycopg2.OperationalError:
        st.error(
            "No se pudo conectar al servidor PostgreSQL. "
            "Verifica que el servicio esté activo, el puerto sea correcto y las credenciales coincidan."
        )
    except psycopg2.Error as error_bd:
        st.error(f"Error en la base de datos al probar la conexión: {error_bd.pgerror or error_bd}")

st.divider()

# Sección 2: Métricas generales y consulta de registros (siempre visibles)
try:
    # Una sola consulta para calcular total de registros y registros activos (disponible = TRUE)
    _, conteos = consultar("SELECT count(*), count(*) FILTER (WHERE disponible) FROM libros;")
    total_registros, registros_activos = conteos[0]

    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Registros en la tabla", total_registros)
    col_m2.metric("Registros con estado activo", registros_activos)

    st.subheader("Registros")

    # Selector de categoría con 'Todas' y las 5 categorías permitidas del Escenario 2
    categorias_opciones = [
        "Todas",
        "Programación",
        "Bases De Datos",
        "Redes",
        "Matemáticas",
        "Inteligencia Artificial",
    ]
    categoria_seleccionada = st.selectbox("Categoría:", categorias_opciones)

    # Construcción de la consulta parametrizada según la categoría elegida
    if categoria_seleccionada == "Todas":
        consulta_libros = """
            SELECT id_libro, codigo_libro, titulo, categoria, costo, ejemplares, disponible
            FROM libros
            ORDER BY id_libro;
        """
        parametros_consulta = ()
    else:
        consulta_libros = """
            SELECT id_libro, codigo_libro, titulo, categoria, costo, ejemplares, disponible
            FROM libros
            WHERE categoria = %s
            ORDER BY id_libro;
        """
        parametros_consulta = (categoria_seleccionada,)

    _, filas_libros = consultar(consulta_libros, parametros_consulta)

    # Formatear filas convirtiendo 'costo' (Decimal) a float() para evitar problemas en Streamlit
    datos_formateados = []
    for fila in filas_libros:
        datos_formateados.append(
            {
                "id": fila[0],
                "código": fila[1],
                "nombre": fila[2],
                "categoría": fila[3],
                "precio": float(fila[4]),
                "existencia": fila[5],
                "estado": fila[6],
            }
        )

    st.dataframe(datos_formateados, hide_index=True, use_container_width=True)

except ValueError as error_val:
    st.error(f"Error de configuración: {error_val}")
    st.error("Revisa el usuario o contraseña")
except psycopg2.OperationalError:
    st.error(
        "No se pudo establecer conexión con PostgreSQL para cargar los registros. "
        "Revisa el host, puerto, usuario o contraseña en tu archivo .env."
    )
except psycopg2.Error as error_bd:
    st.error(f"Error de base de datos al consultar los registros: {error_bd.pgerror or error_bd}")