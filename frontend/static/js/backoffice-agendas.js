document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("agenda-modal");
    const form = document.getElementById("agenda-form");

    const titulo = document.getElementById("agenda-modal-title");
    const botonGuardar = document.getElementById("agenda-submit-btn");

    const campoMedico = document.getElementById("agenda-medico-id");
    const campoConsultorio = document.getElementById("agenda-consultorio");
    const campoDia = document.getElementById("agenda-dia");
    const campoInicio = document.getElementById("agenda-inicio");
    const campoFin = document.getElementById("agenda-fin");
    const campoDuracion = document.getElementById("agenda-duracion");

    const accionCrear = form.action;

    /*
     * Genera horarios cada 15 minutos.
     * Ejemplo: 09:00, 09:15, 09:30, 09:45.
     */
    function generarHorarios() {

        const horarios = [];

        const horaApertura = 7 * 60;
        const horaCierre = 18 * 60;

        for (
            let minutos = horaApertura;
            minutos <= horaCierre;
            minutos += 15
        ) {

            const hora = Math.floor(minutos / 60);
            const minuto = minutos % 60;

            const valor =
                `${String(hora).padStart(2, "0")}:` +
                `${String(minuto).padStart(2, "0")}`;

            horarios.push({
                valor: valor,
                texto: valor
            });

        }

        return horarios;
    }

    const horarios = generarHorarios();

    /*
     * Carga las opciones de hora de inicio.
     */
    function cargarHorariosInicio() {

        campoInicio.innerHTML = '<option value="">Desde</option>';

        horarios.forEach(horario => {

            const opcion = document.createElement("option");

            opcion.value = horario.valor;
            opcion.textContent = horario.texto;

            campoInicio.appendChild(opcion);

        });

    }

    /*
     * Carga únicamente horarios posteriores al inicio.
     */
    function cargarHorariosFin(horaInicio, horaFinSeleccionada = "") {

        campoFin.innerHTML = '<option value="">Hasta</option>';

        if (!horaInicio) {
            campoFin.disabled = true;
            return;
        }

        const horaInicioMinutos = convertirAMinutos(horaInicio);

        horarios.forEach(horario => {

            const horaMinutos = convertirAMinutos(horario.valor);

            if (horaMinutos <= horaInicioMinutos) {
                return;
            }

            const opcion = document.createElement("option");

            opcion.value = horario.valor;
            opcion.textContent = horario.texto;

            campoFin.appendChild(opcion);

        });

        campoFin.disabled = false;

        if (horaFinSeleccionada) {
            campoFin.value = horaFinSeleccionada;
        }

    }

    /*
     * Convierte HH:MM a minutos desde las 00:00.
     */
    function convertirAMinutos(horario) {

        const [hora, minuto] = horario.split(":").map(Number);

        return hora * 60 + minuto;

    }

    /*
     * Normaliza valores como 09:00:00 a 09:00.
     */
    function normalizarHorario(horario) {

        if (!horario) {
            return "";
        }

        return String(horario).trim().slice(0, 5);

    }

    /*
     * Al cambiar el inicio, se recalculan las opciones de finalización.
     */
    campoInicio.addEventListener("change", () => {

        cargarHorariosFin(campoInicio.value);

    });

    /*
     * Preparación inicial de los selectores.
     */
    cargarHorariosInicio();
    cargarHorariosFin("");

    /*
     * Nuevo bloque horario.
     */
    document.getElementById("nuevo-bloque-btn").addEventListener("click", () => {

        form.reset();

        form.action = accionCrear;

        cargarHorariosInicio();
        cargarHorariosFin("");

        titulo.textContent = "Nuevo bloque horario";
        botonGuardar.textContent = "Guardar bloque";

    });

    /*
     * Edición de un bloque existente.
     */
    modal.addEventListener("show.bs.modal", (event) => {

        const boton = event.relatedTarget;

        if (!boton.dataset.agendaId) {
            return;
        }

        form.action = boton.dataset.editUrl;

        campoMedico.value = boton.dataset.medicoId;
        campoConsultorio.value = boton.dataset.consultorioId;
        campoDia.value = boton.dataset.dia;

        const horaInicio = normalizarHorario(boton.dataset.inicio);
        const horaFin = normalizarHorario(boton.dataset.fin);

        cargarHorariosInicio();

        campoInicio.value = horaInicio;

        cargarHorariosFin(horaInicio, horaFin);

        campoDuracion.value = boton.dataset.duracion;

        titulo.textContent = "Editar bloque horario";
        botonGuardar.textContent = "Guardar cambios";

    });

    /*
     * Validación adicional antes de enviar el formulario.
     */
    form.addEventListener("submit", (event) => {

        const inicio = campoInicio.value;
        const fin = campoFin.value;

        if (
            !inicio ||
            !fin ||
            convertirAMinutos(fin) <= convertirAMinutos(inicio)
        ) {

            event.preventDefault();

            alert("La hora de finalización debe ser posterior a la hora de inicio.");

        }

    });

});