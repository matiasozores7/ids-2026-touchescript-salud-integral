
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-fecha-hora");
    const fechas = document.querySelectorAll('input[name="fecha"]');
    const horarios = document.getElementById("horarios");
    const horariosVacio = document.getElementById("horarios-vacio");
    const turnoId = document.getElementById("turno_id");
    const btnContinuar = document.getElementById("btn-continuar");

    const opcionesHorario = document.querySelectorAll("#horarios .col");

    function actualizarHorarios() {
        const fechaSeleccionada =
            document.querySelector('input[name="fecha"]:checked');

        document.querySelectorAll('input[name="hora"]').forEach(input => {
            input.checked = false;
        });

        turnoId.value = "";
        btnContinuar.disabled = true;

        if (!fechaSeleccionada) {
            horarios.hidden = true;
            horariosVacio.hidden = false;
            return;
        }

        let hayHorarios = false;

        opcionesHorario.forEach(opcion => {
            const coincide =
                opcion.dataset.fecha === fechaSeleccionada.value;

            opcion.hidden = !coincide;

            if (coincide) hayHorarios = true;
        });

        horarios.hidden = !hayHorarios;
        horariosVacio.hidden = hayHorarios;

        if (!hayHorarios) {
            horariosVacio.textContent =
                "No hay horarios disponibles para esta fecha.";
        }
    }

    fechas.forEach(fecha => {
        fecha.addEventListener("change", actualizarHorarios);
    });

    document.querySelectorAll('input[name="hora"]').forEach(hora => {
        hora.addEventListener("change", () => {
            turnoId.value = hora.dataset.turnoId;
            btnContinuar.disabled = !turnoId.value;
        });
    });

    form.addEventListener("submit", event => {
        if (!turnoId.value) {
            event.preventDefault();
        }
    });
});
