CREATE DATABASE IF NOT EXISTS librosdash;
USE librosdash;

CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(100) UNIQUE
);


CREATE TABLE rating (
    id_rating INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rating VARCHAR(20) UNIQUE
);

CREATE TABLE libros (
    id_libro INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255),
    precio DECIMAL(10,2),
    id_categoria INT,
    id_rating INT,
    stock_disponible INT,
    url_libro TEXT,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
    FOREIGN KEY (id_rating) REFERENCES rating(id_rating)
);


