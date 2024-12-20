CREATE DATABASE IF NOT EXISTS Spotifind;

USE Spotifind;

CREATE TABLE IF NOT EXISTS Usuarios (
    nombre VARCHAR(50) NOT NULL,
    display_name VARCHAR(100),
    PRIMARY KEY (nombre), 
    ruta_imagen LONGBLOB 
);

CREATE TABLE IF NOT EXISTS mensajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_name VARCHAR(255) NOT NULL,
    username VARCHAR(50) NOT NULL,
    user_id VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Opciones (
        user_id VARCHAR(200) PRIMARY KEY,
        cuerpo_categoria VARCHAR(50),
        ojos_categoria VARCHAR(50),
        ojos_color VARCHAR(50),
        camiseta_categoria VARCHAR(50),
        camiseta_color VARCHAR(50),
        boca VARCHAR(50),
        gafas VARCHAR(50),
        pelo_categoria VARCHAR(50),
        pelo_color VARCHAR(50),
        pantalones_categoria VARCHAR(50),
        pantalones_color VARCHAR(50),
        zapatillas VARCHAR(50),
        accesorio VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Bloqueos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bloqueador VARCHAR(200),
    bloqueado VARCHAR(200),
    UNIQUE(bloqueador, bloqueado)
);

CREATE TABLE IF NOT EXISTS Administradores (
    nombre VARCHAR(100) NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    PRIMARY KEY (nombre)
);


INSERT INTO Administradores (nombre, contrasena)
VALUES 
('admin1', 'contrasena1'),
('admin2', 'contrasena2');






