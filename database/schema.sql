CREATE DATABASE IF NOT EXISTS salud_integral
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE salud_integral;

SET FOREIGN_KEY_CHECKS = 0;

-- Borrar tablas si ya existen
DROP TABLE IF EXISTS turnos;
DROP TABLE IF EXISTS agendas;
DROP TABLE IF EXISTS consultorios;
DROP TABLE IF EXISTS medicos;
DROP TABLE IF EXISTS especialidades;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS coberturas;

SET FOREIGN_KEY_CHECKS = 1;

-- 1. Tabla de Coberturas
CREATE TABLE coberturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- 2. Tabla de Usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('paciente', 'admin', 'recepcionista') NOT NULL,
    cobertura_id INT,
    FOREIGN KEY (cobertura_id) REFERENCES coberturas(id)
);

-- 3. Tabla de Especialidades Médicas
CREATE TABLE especialidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- 4. Tabla de Médicos
CREATE TABLE medicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    especialidad_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (especialidad_id) REFERENCES especialidades(id)
);

-- 5. Tabla de Consultorios
CREATE TABLE consultorios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_sala VARCHAR(20) NOT NULL,
    piso VARCHAR(20)
);

-- 6. Tabla de Agendas
CREATE TABLE agendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medico_id INT NOT NULL,
    consultorio_id INT NOT NULL,
    dia_semana ENUM('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo') NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    duracion_turno INT NOT NULL,
    FOREIGN KEY (medico_id) REFERENCES medicos(id),
    FOREIGN KEY (consultorio_id) REFERENCES consultorios(id)
);

-- 7. Tabla de Turnos
CREATE TABLE turnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medico_id INT NOT NULL,
    paciente_id INT,
    consultorio_id INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    estado ENUM('disponible', 'reservado', 'confirmado', 'atendido', 'cancelado', 'ausente') DEFAULT 'disponible',
    qr_token VARCHAR(255) UNIQUE, 
    FOREIGN KEY (medico_id) REFERENCES medicos(id),
    FOREIGN KEY (paciente_id) REFERENCES usuarios(id),
    FOREIGN KEY (consultorio_id) REFERENCES consultorios(id)
);