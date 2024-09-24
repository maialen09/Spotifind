CREATE DATABASE IF NOT EXISTS SpotifusNueva;

USE SpotifusNueva;


CREATE TABLE IF NOT EXISTS Usuarios (
    nombre VARCHAR(50) NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    PRIMARY KEY (nombre), 
    ruta_imagen LONGBLOB NOT NULL
);

CREATE TABLE IF NOT EXISTS mensajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_name VARCHAR(255) NOT NULL,
    username VARCHAR(50) NOT NULL,
    user_id VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);




