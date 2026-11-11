USE salud_integral;

INSERT INTO coberturas (nombre) VALUES 
('OSDE'), 
('Swiss Medical'), 
('IOMA'), 
('Particular');

INSERT INTO usuarios
    (nombre, apellido, email, telefono, password_hash, rol, activo)
VALUES
('Admin', 'Sistema', 'admin@clinica.com', '11 4000-0001', 'hash_admin_123', 'admin', TRUE),
('Recepción', 'Uno', 'recepcion@clinica.com', '11 4000-0002', 'hash_recepcion_123', 'admin', TRUE),
('Roberto', 'Fernández', 'roberto@clinica.com', '11 4000-0003', 'hash_medico_123', 'medico', TRUE),
('Juan', 'Perez', 'juan@mail.com', '11 4000-0004', 'hash_paciente_1', 'paciente', TRUE),
('Ana', 'Gomez', 'ana@mail.com', '11 4000-0005', 'hash_paciente_2', 'paciente', TRUE);
      

INSERT INTO pacientes (usuario_id, cobertura_id) VALUES 
(4, 1),
(5, 4);

INSERT INTO especialidades (nombre, descripcion) VALUES 
('Clínica Médica', 'Atención integral de pacientes adultos'),
('Cardiología', 'Diagnóstico y tratamiento de enfermedades cardiovasculares');

INSERT INTO medicos (usuario_id, especialidad_id, matricula) VALUES
(3, 1, 'MN 100001');

INSERT INTO medicos_coberturas (medico_id, cobertura_id) VALUES
(1, 1),
(1, 2),
(1, 4);

INSERT INTO consultorios (numero_sala, piso) VALUES 
('101A', '1'), 
('205B', '2');

INSERT INTO agendas (medico_id, consultorio_id, dia_semana, hora_inicio, hora_fin, duracion_turno) 
VALUES (1, 1, 'Lunes', '09:00:00', '13:00:00', 30);

-- 1 de diciembre
INSERT INTO turnos (medico_id, paciente_id, consultorio_id, fecha_hora, estado, qr_token)
VALUES
(1, NULL, 1, '2026-12-01 09:00:00', 'disponible', NULL),
(1, NULL, 1, '2026-12-01 09:30:00', 'disponible', NULL),
(1, 1, 1, '2026-12-01 10:00:00', 'reservado', 'qr_test_001'),
(1, 2, 1, '2026-12-01 10:30:00', 'confirmado', 'qr_test_002');

-- 3 de diciembre
INSERT INTO turnos (medico_id, paciente_id, consultorio_id, fecha_hora, estado, qr_token)
VALUES
(1, NULL, 1, '2026-12-03 09:00:00', 'disponible', NULL),
(1, 1, 1, '2026-12-03 09:30:00', 'reservado', 'qr_test_003'),
(1, NULL, 1, '2026-12-03 10:00:00', 'disponible', NULL),
(1, 2, 1, '2026-12-03 10:30:00', 'confirmado', 'qr_test_004');

-- 7 de diciembre
INSERT INTO turnos (medico_id, paciente_id, consultorio_id, fecha_hora, estado, qr_token)
VALUES
(1, NULL, 1, '2026-12-07 08:30:00', 'disponible', NULL),
(1, 2, 1, '2026-12-07 09:00:00', 'reservado', 'qr_test_005'),
(1, NULL, 1, '2026-12-07 09:30:00', 'disponible', NULL),
(1, 1, 1, '2026-12-07 10:00:00', 'confirmado', 'qr_test_006');

-- 10 de diciembre
INSERT INTO turnos (medico_id, paciente_id, consultorio_id, fecha_hora, estado, qr_token)
VALUES
(1, NULL, 1, '2026-12-10 09:00:00', 'disponible', NULL),
(1, 1, 1, '2026-12-10 09:30:00', 'reservado', 'qr_test_007'),
(1, 2, 1, '2026-12-10 10:00:00', 'confirmado', 'qr_test_008'),
(1, NULL, 1, '2026-12-10 10:30:00', 'disponible', NULL);

-- 14 de diciembre
INSERT INTO turnos (medico_id, paciente_id, consultorio_id, fecha_hora, estado, qr_token)
VALUES
(1, NULL, 1, '2026-12-14 08:30:00', 'disponible', NULL),
(1, 2, 1, '2026-12-14 09:00:00', 'reservado', 'qr_test_009'),
(1, NULL, 1, '2026-12-14 09:30:00', 'disponible', NULL),
(1, 1, 1, '2026-12-14 10:00:00', 'confirmado', 'qr_test_010');

-- 17 de diciembre
INSERT INTO turnos (medico_id, paciente_id, consultorio_id, fecha_hora, estado, qr_token)
VALUES
(1, NULL, 1, '2026-12-17 09:00:00', 'disponible', NULL),
(1, 1, 1, '2026-12-17 09:30:00', 'reservado', 'qr_test_011'),
(1, 2, 1, '2026-12-17 10:00:00', 'confirmado', 'qr_test_012'),
(1, NULL, 1, '2026-12-17 10:30:00', 'disponible', NULL);

-- 21 de diciembre
INSERT INTO turnos (medico_id, paciente_id, consultorio_id, fecha_hora, estado, qr_token)
VALUES
(1, NULL, 1, '2026-12-21 08:30:00', 'disponible', NULL),
(1, NULL, 1, '2026-12-21 09:00:00', 'disponible', NULL),
(1, 2, 1, '2026-12-21 09:30:00', 'reservado', 'qr_test_013'),
(1, 1, 1, '2026-12-21 10:00:00', 'confirmado', 'qr_test_014');

-- 28 de diciembre
INSERT INTO turnos (medico_id, paciente_id, consultorio_id, fecha_hora, estado, qr_token)
VALUES
(1, NULL, 1, '2026-12-28 09:00:00', 'disponible', NULL),
(1, 1, 1, '2026-12-28 09:30:00', 'reservado', 'qr_test_015'),
(1, NULL, 1, '2026-12-28 10:00:00', 'disponible', NULL),
(1, 2, 1, '2026-12-28 10:30:00', 'confirmado', 'qr_test_016');