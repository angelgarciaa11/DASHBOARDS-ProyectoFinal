CREATE DATABASE IF NOT EXISTS librosdash;
USE librosdash;

CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(100) UNIQUE
);
