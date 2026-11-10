# Estado de Integración de Turnos (ABM)

Este documento detalla el estado de la integración del módulo de **Turnos (ABM)** entre el Frontend (Flask SSR en puerto 5001) y el Backend (API REST Flask en puerto 5000), desarrollado en la rama `feat/integracion-turnos`.

---

## 1. Módulos y Funcionalidades Integradas y Testeadas

Se implementó el servicio modular `frontend/app/services/turno_service.py` y se actualizaron las rutas en `frontend/app/routes/patient_route.py` y `frontend/app/routes/backoffice_route.py`, cumpliendo estrictamente con las directivas de `AGENTS.md` (comunicación exclusiva mediante `requests` del lado del servidor, cero peticiones JS en el navegador, manejo de estados con mensajes flash y redirecciones limpias):

1. **Mis Turnos (`GET /mis-turnos`):**
   - Consume en vivo `GET /api/turnos/mis-turnos`.
   - Clasificación dinámica en dos pestañas:
     - **Próximos:** Turnos con estado `reservado` o `confirmado`.
     - **Historial:** Turnos con estado `atendido`, `cancelado` o `ausente`.
   - Formateo amigable en español de fechas, horarios, iniciales y profesionales asignados.
   - Enlace directo a detalle y a código QR digital.

2. **Detalle del Turno (`GET /mis-turnos/<id>`):**
   - Muestra la información completa del turno: código de turno, fecha larga, horario, duración, estado con pill visual, médico, especialidad, consultorio y piso, estado de llegada y recomendaciones.
   - Opciones activas: botón para ver QR y modal de cancelación para turnos en curso.

3. **QR Digital de Check-in (`GET /qr/<id>`):**
   - Consume en vivo `GET /api/turnos/<id>/qr` para obtener el `qr_token` generado por el backend.
   - Muestra el comprobante con el token real para que el paciente lo presente en recepción.

4. **Cancelación de Turnos (`POST /mis-turnos/<id>/cancelar`):**
   - Conectado al modal de confirmación en el frontend.
   - Consume `PATCH /api/turnos/<id>/cancelar`.
   - Libera el turno, actualiza el estado a `cancelado` en el backend y notifica al usuario con un mensaje flash.

5. **Check-in en Recepción / Backoffice (`POST /backoffice/check-in`):**
   - El personal de recepción ingresa el código del comprobante QR.
   - Consume `POST /api/turnos/checkin`.
   - Valida la ventana horaria (±15 minutos respecto de la hora del turno) y el estado del turno. Si es válido, lo marca como `confirmado` e ingresa al paciente a la sala de espera. Ante turnos expirados o códigos inválidos, muestra la alerta descriptiva correspondiente emitida por el backend.

6. **Home del Paciente (`GET /pacientes`):**
   - La tarjeta de "Próximo turno" refleja automáticamente el turno más próximo del paciente autenticado con accesos directos al detalle y a su QR.

7. **Asistente de Reserva de Turnos (`/reservar-turno`) - 100% Operativo de Punta a Punta:**
   - **Paso 1 (Especialidades):** Lista en vivo las especialidades de la base de datos vía `GET /api/especialidades`.
   - **Paso 2 (Médicos):** Filtra los médicos por la especialidad seleccionada vía `GET /api/medicos?especialidad_id=<id>`.
   - **Paso 3 (Fecha y Hora):** Consulta los turnos generados disponibles del profesional vía `GET /api/medicos/<id>/turnos-disponibles`, mostrando las fechas con cupos libres y los horarios asociados a su respectivo `turno_id`.
   - **Paso 4 (Confirmación):** Muestra el resumen del turno (médico, especialidad, fecha, hora) antes de confirmar.
   - **Paso 5 (Reserva):** Envía el `turno_id` seleccionado a `POST /api/turnos`, efectúa la reserva en la base de datos y redirige a "Mis turnos" con mensaje de confirmación exitosa.

---

## 2. Soluciones Implementadas para los Puntos A, B y C

### A. Permisos en Especialidades (`GET /api/especialidades`) — *Resuelto*
- Se actualizó el decorador de control de acceso en `backend/src/routes/especialidades_route.py` a `@validar_rol("admin", "paciente")`.
- Los pacientes autenticados pueden ahora consultar las especialidades sin recibir error 403 Forbidden.

### B. Listado de Médicos por Especialidad (`GET /api/medicos`) — *Resuelto*
- Se habilitó el rol `paciente` en `backend/src/routes/medico_route.py` (`@validar_rol("admin", "paciente")`).
- Se agregó el soporte para el parámetro opcional `especialidad_id` en repositorio, servicio y ruta (`GET /api/medicos?especialidad_id=<id>`), permitiendo filtrar profesionales por especialidad respetando consultas SQL parametrizadas seguras.

### C. Consulta de Turnos Disponibles para Reserva — *Resuelto*
- Se implementó el endpoint `GET /api/medicos/<int:medico_id>/turnos-disponibles` con soporte opcional de filtro por `?fecha=YYYY-MM-DD`.
- Devuelve los turnos pre-generados con estado `'disponible'` junto a su `id`, horario y consultorio, permitiendo al frontend asociar el slot exacto (`turno_id`) para enviar al confirmar la reserva en `POST /api/turnos`.

### D. Validaciones Temporales (Bloqueo de Turnos Pasados) — *Resuelto*
- **Listado de disponibles:** Se incorporó la condición SQL `AND t.fecha_hora > NOW()` en `obtener_turnos_disponibles` y un filtro en el frontend para evitar que turnos cuya fecha y hora ya pasaron se muestren al paciente.
- **Reserva de turnos:** En `reservar_turno` (`turno_service.py`), se agregó la validación que rechaza con `ConflictError` (409) cualquier intento de reservar un turno cuya `fecha_hora <= datetime.now()`.
- **Generación de turnos:** En `validar_generacion_turnos`, se valida que la `fecha_fin` no sea anterior a la fecha actual (`BadRequestError`), y en el generador de slots se omiten automáticamente aquellos horarios que hayan quedado en el pasado dentro del día de hoy.

---

## 3. Próximas Mejoras Sugeridas (Backlog)

1. **Endpoint Directo para Consulta Individual de Turno (`GET /api/turnos/<id>`):**
   - Actualmente el frontend lo resuelve consultando el listado del paciente y filtrando por ID. Exponer este endpoint directamente optimizará las peticiones individuales.
2. **Eliminación de Campos No Relacionales (DNI) y Coberturas Dinámicas:**
   - Retirar el campo `DNI` en plantillas del frontend donde aún figure, ya que no existe en el esquema SQL.
   - Implementar `GET /api/coberturas` para poblar el selector de obras sociales desde la base de datos.
