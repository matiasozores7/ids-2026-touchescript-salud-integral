
USE salud_integral;

-- =====================================================
-- 1. COBERTURAS
-- =====================================================

INSERT INTO coberturas (nombre) VALUES
('OSDE'),
('Swiss Medical'),
('IOMA'),
('Particular'),
('Galeno');

-- =====================================================
-- 2. USUARIOS
-- =====================================================

INSERT INTO usuarios
    (nombre, apellido, email, telefono, password_hash, rol, activo)
VALUES
-- Administradores
('Admin', 'Sistema', 'admin@clinica.com', '11 4000-0001', 'hash_admin_123', 'admin', TRUE),
('Recepcion', 'Principal', 'recepcion@clinica.com', '11 4000-0002', 'hash_recepcion_123', 'admin', TRUE),

-- Médicos
('Roberto', 'Fernandez', 'roberto@clinica.com', '11 4000-0003', 'hash_medico_1', 'medico', TRUE),
('Laura', 'Martinez', 'laura@clinica.com', '11 4000-0004', 'hash_medico_2', 'medico', TRUE),
('Carlos', 'Gonzalez', 'carlos@clinica.com', '11 4000-0005', 'hash_medico_3', 'medico', TRUE),
('Mariana', 'Lopez', 'mariana@clinica.com', '11 4000-0006', 'hash_medico_4', 'medico', TRUE),
('Diego', 'Ramirez', 'diego@clinica.com', '11 4000-0007', 'hash_medico_5', 'medico', FALSE),

-- Pacientes
('Juan', 'Perez', 'juan@mail.com', '11 4000-0010', 'hash_paciente_1', 'paciente', TRUE),
('Ana', 'Gomez', 'ana@mail.com', '11 4000-0011', 'hash_paciente_2', 'paciente', TRUE),
('Lucia', 'Fernandez', 'lucia@mail.com', '11 4000-0012', 'hash_paciente_3', 'paciente', TRUE),
('Martin', 'Rodriguez', 'martin@mail.com', '11 4000-0013', 'hash_paciente_4', 'paciente', TRUE),
('Sofia', 'Diaz', 'sofia@mail.com', '11 4000-0014', 'hash_paciente_5', 'paciente', TRUE),
('Pedro', 'Sanchez', 'pedro@mail.com', '11 4000-0015', 'hash_paciente_6', 'paciente', TRUE),
('Valentina', 'Torres', 'valentina@mail.com', '11 4000-0016', 'hash_paciente_7', 'paciente', TRUE),
('Nicolas', 'Alvarez', 'nicolas@mail.com', '11 4000-0017', 'hash_paciente_8', 'paciente', TRUE),
('Camila', 'Romero', 'camila@mail.com', '11 4000-0018', 'hash_paciente_9', 'paciente', TRUE),
('Federico', 'Acosta', 'federico@mail.com', '11 4000-0019', 'hash_paciente_10', 'paciente', TRUE),
('Julieta', 'Herrera', 'julieta@mail.com', '11 4000-0020', 'hash_paciente_11', 'paciente', TRUE),
('Agustin', 'Morales', 'agustin@mail.com', '11 4000-0021', 'hash_paciente_12', 'paciente', FALSE),

-- Usuarios de prueba con contraseña hasheada
('Paciente', 'Demo', 'paciente.demo@clinica.com', '11 4000-0030', 'scrypt:32768:8:1$zVnd4N2CwEgYG1iF$37003090a8833c5f3a3abfd242eefe87d5d3e2b142ba3ecf807a76228034851ff36d434b5acc5dd473d9bdd1b178b07deb459f7ceca6b3236ef7cbaf106ca672', 'paciente', TRUE), -- Contraseña: Paciente123!
('Administrador', 'Demo', 'admin.demo@clinica.com', '11 4000-0031', 'scrypt:32768:8:1$91tP9zUKZw32YklH$563b889be82f37a3489c41fef7cf095e6812fc61d31fc3590b0fe5e7f0ba8186abd9746896ef368c8bf5e40d95afd0d76646683540a8920191c458433f8afcf6', 'admin', TRUE); -- Contraseña: Admin123!

-- =====================================================
-- 3. PACIENTES
-- =====================================================

INSERT INTO pacientes (usuario_id, cobertura_id) VALUES
(8, 1),
(9, 2),
(10, 1),
(11, 3),
(12, 4),
(13, 2),
(14, 5),
(15, 1),
(16, 3),
(17, 4),
(18, 2),
(19, 5),
(20, 1);

-- =====================================================
-- 4. ESPECIALIDADES
-- =====================================================

INSERT INTO especialidades (nombre, descripcion) VALUES
('Clinica Medica', 'Atencion integral y seguimiento de pacientes adultos'),
('Cardiologia', 'Diagnostico y tratamiento de enfermedades cardiovasculares'),
('Dermatologia', 'Diagnostico y tratamiento de enfermedades de la piel'),
('Traumatologia', 'Diagnostico y tratamiento de lesiones osteomusculares');

-- =====================================================
-- 5. MEDICOS
-- =====================================================

INSERT INTO medicos (usuario_id, especialidad_id, matricula) VALUES
(3, 1, 'MN 100001'),
(4, 2, 'MN 100002'),
(5, 3, 'MN 100003'),
(6, 4, 'MN 100004'),
(7, 1, 'MN 100005');

-- =====================================================
-- 6. COBERTURAS DE MEDICOS
-- =====================================================

INSERT INTO medicos_coberturas (medico_id, cobertura_id) VALUES
(1, 1), (1, 2), (1, 4),
(2, 1), (2, 2), (2, 5),
(3, 2), (3, 3), (3, 4),
(4, 1), (4, 3), (4, 5),
(5, 1), (5, 4);

-- =====================================================
-- 7. CONSULTORIOS
-- =====================================================

INSERT INTO consultorios (numero_sala, piso, activo) VALUES
('101A', '1', TRUE),
('102B', '1', TRUE),
('205A', '2', TRUE),
('206B', '2', TRUE),
('301A', '3', FALSE);
