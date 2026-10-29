USE salud_integral;

INSERT INTO coberturas (nombre) VALUES 
('OSDE'), 
('Swiss Medical'), 
('IOMA'), 
('Particular');

INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES 
('Admin Sistema', 'admin@clinica.com', 'hash_admin_123', 'admin'),         
('Recepción Uno', 'recepcion@clinica.com', 'hash_recepcion_123', 'recepcionista'), 
('Dr. Roberto Fernández', 'roberto@clinica.com', 'hash_medico_123', 'medico'),   
('Juan Perez', 'juan@mail.com', 'hash_paciente_1', 'paciente'),                  
('Ana Gomez', 'ana@mail.com', 'hash_paciente_2', 'paciente');                   

INSERT INTO pacientes (usuario_id, cobertura_id) VALUES 
(4, 1),
(5, 4);

INSERT INTO especialidades (nombre, descripcion) VALUES 
('Clínica Médica', 'Atención integral de pacientes adultos'),
('Cardiología', 'Diagnóstico y tratamiento de enfermedades cardiovasculares');

INSERT INTO medicos (usuario_id, especialidad_id) VALUES 
(3, 1);

INSERT INTO consultorios (numero_sala, piso) VALUES 
('101A', '1'), 
('205B', '2');

INSERT INTO agendas (medico_id, consultorio_id, dia_semana, hora_inicio, hora_fin, duracion_turno) 
VALUES (1, 1, 'Lunes', '09:00:00', '13:00:00', 30);

INSERT INTO turnos (medico_id, paciente_id, consultorio_id, fecha_hora, estado, qr_token) 
VALUES (1, NULL, 1, '2026-11-02 09:00:00', 'disponible', NULL);

INSERT INTO turnos (medico_id, paciente_id, consultorio_id, fecha_hora, estado, qr_token) 
VALUES (1, 1, 1, '2026-11-02 09:30:00', 'reservado', 'qr_juan_abc123');

INSERT INTO turnos (medico_id, paciente_id, consultorio_id, fecha_hora, fecha_hora_llegada, estado, qr_token) 
VALUES (1, 2, 1, '2026-11-02 10:00:00', '2026-11-02 09:55:00', 'confirmado', 'qr_ana_xyz789');