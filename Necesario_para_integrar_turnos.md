# Necesario para Integrar Turnos

Este documento detalla el estado de la integración del módulo de **Turnos (ABM)** entre el Frontend (Flask SSR en puerto 5001) y el Backend (API REST Flask en puerto 5000), especificando las funcionalidades operativas testeadas y los requisitos pendientes en el Backend para completar el flujo de reserva de turnos de punta a punta.

---

## 1. Módulos y Funcionalidades Integradas y Testeadas

Se implementó el servicio modular `frontend/app/services/turno_service.py` y se actualizaron las rutas en `frontend/app/routes/patient_route.py` y `frontend/app/routes/backoffice_route.py`, cumpliendo estrictamente con las directivas de `AGENTS.md` (comunicación exclusiva mediante `requests` del lado del servidor, cero lógica en el navegador, manejo de estados con mensajes flash y redirecciones limpias):

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

---

## 2. Puntos Pendientes en el Backend para Completar el Asistente de Reserva (`/reservar-turno`)

El asistente de reserva consta de 4 pasos (`especialidad` $\rightarrow$ `medico` $\rightarrow$ `fecha-hora` $\rightarrow$ `confirmacion` $\rightarrow$ `resultado`). Actualmente el frontend tiene la interfaz y las rutas preparadas, pero la integración completa con la base de datos se encuentra bloqueada por las siguientes razones en los endpoints del Backend:

### A. Permisos en Especialidades (`GET /api/especialidades`)
- **Situación actual:** La ruta en `backend/src/routes/especialidades_route.py` está protegida con `@validar_rol("admin")`.
- **Problema:** Cuando un usuario con rol `paciente` intenta consultar las especialidades para iniciar una reserva, el backend responde con un error `403 Forbidden` (`ForbiddenError: Acceso no autorizado para el rol actual`).
- **Solución requerida:** Permitir el rol `paciente` en la ruta (`@validar_rol("admin", "paciente")`) o crear un endpoint público/abierto a usuarios autenticados para consulta de especialidades activas.

### B. Listado de Médicos por Especialidad (`GET /api/medicos`)
- **Situación actual:** `GET /api/medicos` está restringido con `@validar_rol("admin")` y no acepta filtro por `especialidad_id`. Tampoco existe el recurso `/api/especialidades/<id>/medicos`.
- **Problema:** En el Paso 2 de la reserva, el paciente no puede obtener la lista de médicos que atienden la especialidad seleccionada.
- **Solución requerida:**
  - Permitir a los pacientes listar médicos.
  - Implementar el filtro opcional por especialidad: `GET /api/medicos?especialidad_id=<id>` o el endpoint `GET /api/especialidades/<id>/medicos`.

### C. Consulta de Turnos Disponibles para Reserva (`GET /api/turnos`)
- **Situación actual:**
  - El backend cuenta con `GET /api/medicos/<id>/dias-disponibles` y `GET /api/medicos/<id>/horarios-disponibles?fecha=YYYY-MM-DD`, pero estos endpoints solo devuelven los días y rangos horarios teóricos configurados en la tabla `agendas`. No devuelven registros de la tabla `turnos`.
  - Sin embargo, para efectuar una reserva, el endpoint `POST /api/turnos` exige obligatoriamente recibir el parámetro `turno_id`:
    ```json
    { "turno_id": 15 }
    ```
    Y busca un registro pre-generado en la tabla `turnos` con `estado = 'disponible'`.
- **Problema:** El frontend no tiene forma de saber cuáles son los `turno_id` disponibles para un médico en una fecha determinada.
- **Solución requerida:**
  - Crear un endpoint que liste turnos disponibles generados, por ejemplo:
    `GET /api/medicos/<id>/turnos-disponibles?fecha=YYYY-MM-DD` o `GET /api/turnos?estado=disponible&medico_id=<id>&fecha=YYYY-MM-DD` que devuelva los objetos de turno con su respectivo `id`, hora de inicio y estado.

### D. Endpoint Directo para Consulta Individual de Turno (`GET /api/turnos/<id>`)
- **Situación actual:** En `backend/src/repositories/turno_repository.py` existe la función `obtener_turno_con_detalles(connection, turno_id)`, pero no está expuesta a través de ningún endpoint en `backend/src/routes/turno_route.py`.
- **Impacto actual:** El frontend lo resuelve consultando el listado del paciente y buscando por ID.
- **Solución sugerida:** Exponer `GET /api/turnos/<int:turno_id>` con `@validar_rol("paciente", "admin", "medico")` para permitir consultas puntuales más directas y eficientes.

### E. Limpieza de Campos Obsoletos en el Frontend (DNI) y Coberturas Dinámicas
- Tal como se indicó en las observaciones del proyecto:
  - Eliminar el campo `DNI` en las plantillas y formularios que aún lo contengan, ya que no forma parte del modelo relacional en la base de datos.
  - Exponer un endpoint en el backend (`GET /api/coberturas`) para que la selección de obra social/cobertura en el registro y en la reserva provenga de la base de datos y no de listas fijas.

