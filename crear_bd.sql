-- Paso 1: Ejecutar conectado a la base de datos por defecto 'postgres'
-- Crea la base de datos 'biblioteca' con codificación UTF8
CREATE DATABASE biblioteca
    WITH ENCODING 'UTF8'
    TEMPLATE template0;

-- Paso 2: Conectarse a la base de datos 'biblioteca' y ejecutar
-- Creación de la tabla principal 'libros' con 10 columnas y restricciones
CREATE TABLE libros (
    id_libro            SERIAL PRIMARY KEY,
    codigo_libro        VARCHAR(12)  NOT NULL UNIQUE,
    titulo              VARCHAR(100) NOT NULL CHECK (length(trim(titulo)) > 0),
    resumen             TEXT,
    categoria           VARCHAR(30)  NOT NULL CHECK (categoria IN (
                            'Programación',
                            'Bases De Datos',
                            'Redes',
                            'Matemáticas',
                            'Inteligencia Artificial'
                        )),
    costo               NUMERIC(10,2) NOT NULL CHECK (costo > 0),
    ejemplares          INTEGER       NOT NULL DEFAULT 0 CHECK (ejemplares >= 0),
    disponible          BOOLEAN       NOT NULL DEFAULT TRUE,
    fecha_ingreso       DATE          NOT NULL DEFAULT CURRENT_DATE,
    ultima_modificacion TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Índice sobre 'categoria' para optimizar búsquedas
CREATE INDEX idx_libros_categoria ON libros (categoria);
-- Comentario de la tabla en el catálogo del sistema
COMMENT ON TABLE libros IS 'Catálogo de libros de la biblioteca escolar';

-- Inserción de 5 registros con restricciones
-- Fechas de 2025
-- 5 categorías
-- 1 con disponible = FALSE
-- 1 con ejemplares = 0
-- 2 con resumen NULL)
-- Se omite 'ultima_modificacion' para que tome su valor DEFAULT automáticamente
INSERT INTO libros (codigo_libro, titulo, resumen, categoria, costo, ejemplares, disponible, fecha_ingreso)
VALUES
    ('PRG-001', 'Clean Code en Python', 'Guía práctica sobre principios de código limpio y refactorización.', 'Programación', 450.00, 5, TRUE, '2025-02-10'),
    ('BDD-002', 'Fundamentos de Bases de Datos', 'Modelo relacional, álgebra relacional, normalización y SQL.', 'Bases De Datos', 520.50, 3, TRUE, '2025-03-18'),
    ('RED-003', 'Redes de Computadoras', NULL, 'Redes', 380.00, 0, FALSE, '2025-05-22'),
    ('MAT-004', 'Matemáticas Discretas y Combinatoria', NULL, 'Matemáticas', 310.00, 4, TRUE, '2025-08-05'),
    ('IA-005', 'Inteligencia Artificial: Un Enfoque Moderno', 'Búsqueda heurística, aprendizaje automático y redes neuronales.', 'Inteligencia Artificial', 615.75, 2, TRUE, '2025-10-14');

-- Creación del usuario exclusivo de la aplicación (no usar 'postgres')
CREATE USER app_biblioteca WITH PASSWORD 'Biblioteca_segura!';

-- Asignación de permisos mínimos necesarios
GRANT CONNECT ON DATABASE biblioteca TO app_biblioteca;
GRANT USAGE ON SCHEMA public TO app_biblioteca;
GRANT SELECT, INSERT, UPDATE, DELETE ON libros TO app_biblioteca;

-- Permiso sobre la secuencia del campo SERIAL para futuras inserciones en la actividad 3
GRANT USAGE, SELECT ON SEQUENCE libros_id_libro_seq TO app_biblioteca;