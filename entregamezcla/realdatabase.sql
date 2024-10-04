CREATE DATABASE IF NOT EXISTS SpotifusNueva;

USE SpotifusNueva;


CREATE TABLE IF NOT EXISTS Usuarios (
    nombre VARCHAR(50) NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
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

CREATE TABLE IF NOT EXISTS Opciones(
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
)




