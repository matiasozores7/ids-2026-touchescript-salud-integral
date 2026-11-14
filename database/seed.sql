
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
('Agustin', 'Morales', 'agustin@mail.com', '11 4000-0021', 'hash_paciente_12', 'paciente', FALSE);

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
(19, 5);

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

-- =====================================================
-- 8. AGENDAS
-- =====================================================

INSERT INTO agendas
    (medico_id, consultorio_id, dia_semana, hora_inicio, hora_fin, duracion_turno)
VALUES
-- Clinica medica
(1, 1, 'Lunes', '08:00:00', '13:00:00', 30),
(1, 1, 'Miercoles', '08:00:00', '13:00:00', 30),
(1, 1, 'Viernes', '08:00:00', '13:00:00', 30),

-- Cardiologia
(2, 2, 'Lunes', '09:00:00', '14:00:00', 30),
(2, 2, 'Martes', '09:00:00', '14:00:00', 30),
(2, 2, 'Jueves', '09:00:00', '14:00:00', 30),

-- Dermatologia
(3, 3, 'Martes', '08:00:00', '12:00:00', 30),
(3, 3, 'Jueves', '08:00:00', '12:00:00', 30),

-- Traumatologia
(4, 4, 'Lunes', '14:00:00', '18:00:00', 30),
(4, 4, 'Miercoles', '14:00:00', '18:00:00', 30),
(4, 4, 'Viernes', '14:00:00', '18:00:00', 30);

-- =====================================================
-- 9. TURNOS HISTORICOS
-- Ultimos 30 dias
-- =====================================================

INSERT INTO turnos
    (medico_id, paciente_id, consultorio_id, fecha_hora, estado, qr_token)
VALUES

-- Hace 2 dias
(1, 1, 1, DATE_SUB(NOW(), INTERVAL 2 DAY), 'atendido', 'qr_hist_001'),
(1, 2, 1, DATE_SUB(NOW(), INTERVAL 2 DAY) + INTERVAL 30 MINUTE, 'atendido', 'qr_hist_002'),
(2, 3, 2, DATE_SUB(NOW(), INTERVAL 2 DAY) + INTERVAL 1 HOUR, 'ausente', 'qr_hist_003'),
(3, 4, 3, DATE_SUB(NOW(), INTERVAL 2 DAY) + INTERVAL 2 HOUR, 'atendido', 'qr_hist_004'),
(4, 5, 4, DATE_SUB(NOW(), INTERVAL 2 DAY) + INTERVAL 3 HOUR, 'cancelado', 'qr_hist_005'),

-- Hace 5 dias
(1, 6, 1, DATE_SUB(NOW(), INTERVAL 5 DAY), 'atendido', 'qr_hist_006'),
(1, 7, 1, DATE_SUB(NOW(), INTERVAL 5 DAY) + INTERVAL 30 MINUTE, 'ausente', 'qr_hist_007'),
(2, 8, 2, DATE_SUB(NOW(), INTERVAL 5 DAY) + INTERVAL 1 HOUR, 'atendido', 'qr_hist_008'),
(3, 9, 3, DATE_SUB(NOW(), INTERVAL 5 DAY) + INTERVAL 2 HOUR, 'atendido', 'qr_hist_009'),
(4, 10, 4, DATE_SUB(NOW(), INTERVAL 5 DAY) + INTERVAL 3 HOUR, 'atendido', 'qr_hist_010'),

-- Hace 10 dias
(1, 11, 1, DATE_SUB(NOW(), INTERVAL 10 DAY), 'atendido', 'qr_hist_011'),
(2, 12, 2, DATE_SUB(NOW(), INTERVAL 10 DAY) + INTERVAL 30 MINUTE, 'ausente', 'qr_hist_012'),
(3, 1, 3, DATE_SUB(NOW(), INTERVAL 10 DAY) + INTERVAL 1 HOUR, 'atendido', 'qr_hist_013'),
(4, 2, 4, DATE_SUB(NOW(), INTERVAL 10 DAY) + INTERVAL 2 HOUR, 'cancelado', 'qr_hist_014'),

-- Hace 20 dias
(1, 3, 1, DATE_SUB(NOW(), INTERVAL 20 DAY), 'atendido', 'qr_hist_015'),
(2, 4, 2, DATE_SUB(NOW(), INTERVAL 20 DAY) + INTERVAL 30 MINUTE, 'atendido', 'qr_hist_016'),
(3, 5, 3, DATE_SUB(NOW(), INTERVAL 20 DAY) + INTERVAL 1 HOUR, 'ausente', 'qr_hist_017'),
(4, 6, 4, DATE_SUB(NOW(), INTERVAL 20 DAY) + INTERVAL 2 HOUR, 'atendido', 'qr_hist_018');

-- =====================================================
-- 10. TURNOS DE HOY
-- Mezcla de estados para probar el dashboard
-- =====================================================

INSERT INTO turnos
    (medico_id, paciente_id, consultorio_id, fecha_hora, fecha_hora_llegada, estado, qr_token)
VALUES

-- Clinica medica
(1, 1, 1, DATE_SUB(NOW(), INTERVAL 3 HOUR), DATE_SUB(NOW(), INTERVAL 3 HOUR) + INTERVAL 5 MINUTE, 'atendido', 'qr_hoy_001'),
(1, 2, 1, DATE_SUB(NOW(), INTERVAL 2 HOUR), DATE_SUB(NOW(), INTERVAL 2 HOUR) + INTERVAL 10 MINUTE, 'atendido', 'qr_hoy_002'),
(1, 3, 1, DATE_SUB(NOW(), INTERVAL 1 HOUR), DATE_SUB(NOW(), INTERVAL 1 HOUR) + INTERVAL 5 MINUTE, 'confirmado', 'qr_hoy_003'),
(1, 4, 1, DATE_ADD(NOW(), INTERVAL 1 HOUR), NULL, 'reservado', 'qr_hoy_004'),

-- Cardiologia
(2, 5, 2, DATE_SUB(NOW(), INTERVAL 90 MINUTE), DATE_SUB(NOW(), INTERVAL 85 MINUTE), 'atendido', 'qr_hoy_005'),
(2, 6, 2, DATE_SUB(NOW(), INTERVAL 30 MINUTE), NULL, 'ausente', 'qr_hoy_006'),
(2, 7, 2, DATE_ADD(NOW(), INTERVAL 2 HOUR), NULL, 'reservado', 'qr_hoy_007'),

-- Dermatologia
(3, 8, 3, DATE_ADD(NOW(), INTERVAL 3 HOUR), NULL, 'reservado', 'qr_hoy_008'),
(3, 9, 3, DATE_ADD(NOW(), INTERVAL 4 HOUR), NULL, 'reservado', 'qr_hoy_009'),

-- Traumatologia
(4, 10, 4, DATE_ADD(NOW(), INTERVAL 5 HOUR), NULL, 'reservado', 'qr_hoy_010'),
(4, 11, 4, DATE_ADD(NOW(), INTERVAL 6 HOUR), NULL, 'disponible', NULL);

-- =====================================================
-- 11. TURNOS FUTUROS
-- =====================================================

INSERT INTO turnos
    (medico_id, paciente_id, consultorio_id, fecha_hora, estado, qr_token)
VALUES

-- Mañana
(1, 1, 1, DATE_ADD(CURDATE(), INTERVAL 1 DAY) + INTERVAL 9 HOUR, 'reservado', 'qr_fut_001'),
(1, 2, 1, DATE_ADD(CURDATE(), INTERVAL 1 DAY) + INTERVAL 10 HOUR, 'reservado', 'qr_fut_002'),
(1, NULL, 1, DATE_ADD(CURDATE(), INTERVAL 1 DAY) + INTERVAL 11 HOUR, 'disponible', NULL),
(2, 3, 2, DATE_ADD(CURDATE(), INTERVAL 1 DAY) + INTERVAL 9 HOUR, 'reservado', 'qr_fut_003'),
(2, 4, 2, DATE_ADD(CURDATE(), INTERVAL 1 DAY) + INTERVAL 10 HOUR, 'reservado', 'qr_fut_004'),

-- En 3 dias
(1, 5, 1, DATE_ADD(CURDATE(), INTERVAL 3 DAY) + INTERVAL 9 HOUR, 'reservado', 'qr_fut_005'),
(2, 6, 2, DATE_ADD(CURDATE(), INTERVAL 3 DAY) + INTERVAL 10 HOUR, 'reservado', 'qr_fut_006'),
(3, 7, 3, DATE_ADD(CURDATE(), INTERVAL 3 DAY) + INTERVAL 11 HOUR, 'reservado', 'qr_fut_007'),
(4, 8, 4, DATE_ADD(CURDATE(), INTERVAL 3 DAY) + INTERVAL 14 HOUR, 'reservado', 'qr_fut_008'),

-- En 7 dias
(1, 9, 1, DATE_ADD(CURDATE(), INTERVAL 7 DAY) + INTERVAL 9 HOUR, 'reservado', 'qr_fut_009'),
(1, 10, 1, DATE_ADD(CURDATE(), INTERVAL 7 DAY) + INTERVAL 10 HOUR, 'reservado', 'qr_fut_010'),
(2, 11, 2, DATE_ADD(CURDATE(), INTERVAL 7 DAY) + INTERVAL 11 HOUR, 'reservado', 'qr_fut_011'),
(3, 12, 3, DATE_ADD(CURDATE(), INTERVAL 7 DAY) + INTERVAL 12 HOUR, 'reservado', 'qr_fut_012');
