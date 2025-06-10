#TABLA DE PRODUCTOS 
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    precio VARCHAR(50),
    descripcion TEXT,
    categoria VARCHAR(100),
    genero VARCHAR(50),
    color VARCHAR(100),
    talla_disponible VARCHAR(100)
);
CREATE DATABASE IF NOT EXISTS nike_db;
USE nike_db;
#TABLA DE GENEROS DE LOS PRODUCTOS
CREATE TABLE generos (
    id_genero INT AUTO_INCREMENT PRIMARY KEY,
    nombre_genero VARCHAR(50) UNIQUE
);
#CATEGORIAS 
CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(100) UNIQUE
);

CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    precio DECIMAL(10,2),
    id_genero INT,
    id_categoria INT,
    url_producto TEXT,
    FOREIGN KEY (id_genero) REFERENCES generos(id_genero),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS generos;
DROP TABLE IF EXISTS categorias;

CREATE TABLE generos (
    id_genero INT AUTO_INCREMENT PRIMARY KEY,
    nombre_genero VARCHAR(50) UNIQUE
);

CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(100) UNIQUE
);

CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    precio DECIMAL(10,2),
    id_genero INT,
    id_categoria INT,
    url_producto TEXT,
    FOREIGN KEY (id_genero) REFERENCES generos(id_genero),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);
USE nike_db;

SELECT * FROM productos;
SELECT * FROM generos;

CREATE OR REPLACE VIEW vista_productos_completa AS
SELECT 
    p.id_producto,
    p.nombre AS nombre_producto,
    p.precio,
    g.nombre_genero,
    c.nombre_categoria
FROM 
    productos p
JOIN 
    generos g ON p.id_genero = g.id_genero
JOIN 
    categorias c ON p.id_categoria = c.id_categoria;
    
    SELECT * FROM vista_productos_completa;
    #TOTAL DE PRODUCTOS 
    SELECT COUNT(*) AS total_productos FROM vista_productos_completa;
    #TOTAL DE PRODUCTOS POR GENERO 
SELECT nombre_genero, COUNT(*) AS cantidad
FROM vista_productos_completa
GROUP BY nombre_genero;

#*****************************************
CREATE OR REPLACE VIEW vista_resumen_general AS
SELECT
    COUNT(*) AS total_productos,
    SUM(CASE WHEN g.nombre_genero = 'Hombre' THEN 1 ELSE 0 END) AS total_hombre,
    SUM(CASE WHEN g.nombre_genero = 'Mujer' THEN 1 ELSE 0 END) AS total_mujer,
    SUM(CASE WHEN g.nombre_genero = 'Unisex' THEN 1 ELSE 0 END) AS total_unisex,
    COUNT(DISTINCT c.nombre_categoria) AS total_categorias,
    ROUND(AVG(p.precio), 2) AS precio_promedio_general
FROM productos p
JOIN generos g ON p.id_genero = g.id_genero
JOIN categorias c ON p.id_categoria = c.id_categoria;

SELECT * FROM vista_resumen_general;
#*************************VISTAS
CREATE OR REPLACE VIEW vista_resumen_general AS
SELECT 
    COUNT(*) AS total_productos,
    COUNT(DISTINCT p.id_categoria) AS total_categorias,
    COUNT(DISTINCT p.id_genero) AS total_generos,
    ROUND(AVG(p.precio), 2) AS precio_promedio_general
FROM productos p;
#*******************VISTASSSS
CREATE OR REPLACE VIEW vista_precio_categoria_genero AS
SELECT 
    c.nombre_categoria AS categoria,
    g.nombre_genero AS genero,
    COUNT(*) AS total_productos,
    ROUND(AVG(p.precio), 2) AS precio_promedio
FROM productos p
JOIN categorias c ON p.id_categoria = c.id_categoria
JOIN generos g ON p.id_genero = g.id_genero
GROUP BY c.nombre_categoria, g.nombre_genero;

#******************VISTASSSSS
CREATE OR REPLACE VIEW vista_detalle_productos AS
SELECT 
    p.nombre AS nombre_producto,
    c.nombre_categoria AS categoria,
    g.nombre_genero AS genero,
    p.precio
FROM productos p
JOIN categorias c ON p.id_categoria = c.id_categoria
JOIN generos g ON p.id_genero = g.id_genero;

CREATE TABLE sucursales (
    id_sucursal INT AUTO_INCREMENT PRIMARY KEY,
    nombre_sucursal VARCHAR(100),
    ciudad VARCHAR(100),
    estado VARCHAR(100),
    direccion VARCHAR(255)
);
#**************sucursales mexico********************
INSERT INTO sucursales (nombre_sucursal, ciudad, estado, direccion) VALUES
('Nike Store Reforma', 'Ciudad de México', 'CDMX', 'Av. Paseo de la Reforma 222, Cuauhtémoc'),
('Nike Factory Store Perisur', 'Ciudad de México', 'CDMX', 'Anillo Periférico 4690, Coyoacán'),
('Nike Store Santa Fe', 'Ciudad de México', 'CDMX', 'Centro Santa Fe, Vasco de Quiroga 3800'),
('Nike Store Andares', 'Zapopan', 'Jalisco', 'Blvd. Puerta de Hierro 4965, Andares'),
('Nike Factory Store Outlet Guadalajara', 'Tlaquepaque', 'Jalisco', 'Carretera a Chapala 6700, Las Pintas'),
('Nike Store Monterrey', 'Monterrey', 'Nuevo León', 'Av. Ignacio Morones Prieto 2800, Del Valle'),
('Nike Store Galerías Monterrey', 'Monterrey', 'Nuevo León', 'Av. Insurgentes 2500, Mitras Centro'),
('Nike Factory Store Querétaro', 'Querétaro', 'Querétaro', 'Prolongación Zaragoza 99, El Jacal'),
('Nike Store Puebla Angelópolis', 'Puebla', 'Puebla', 'Blvd. del Niño Poblano 2510, Reserva Territorial Atlixcáyotl'),
('Nike Factory Store Cancún', 'Cancún', 'Quintana Roo', 'Blvd. Luis Donaldo Colosio 36, SM 310');

SELECT * FROM sucursales;

CREATE OR REPLACE VIEW vista_precio_categoria_genero AS
SELECT 
    p.nombre,
    p.url_producto,
    p.precio,
    g.nombre_genero AS genero,
    c.nombre_categoria AS categoria
FROM productos p
JOIN generos g ON p.id_genero = g.id_genero
JOIN categorias c ON p.id_categoria = c.id_categoria;


ALTER TABLE productos ADD COLUMN id_categoria INT;

-- Si quieres que no dé errores con los datos existentes, podrías asignarle un valor por defecto o dejarla nula:
ALTER TABLE productos MODIFY id_categoria INT DEFAULT NULL;

-- Luego vuelve a insertar los productos con tu script Python para que se rellene correctamente.


CREATE TABLE IF NOT EXISTS generos (
    id_genero INT AUTO_INCREMENT PRIMARY KEY,
    nombre_genero VARCHAR(50) UNIQUE
);

CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(50) UNIQUE
);

DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS generos;
DROP TABLE IF EXISTS categorias;

CREATE TABLE generos (
    id_genero INT AUTO_INCREMENT PRIMARY KEY,
    nombre_genero VARCHAR(50) UNIQUE
);

CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(50) UNIQUE
);

CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    precio DECIMAL(10,2),
    id_genero INT,
    id_categoria INT,
    url_producto TEXT,
    FOREIGN KEY (id_genero) REFERENCES generos(id_genero),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);
SELECT * FROM productos LIMIT 100;




