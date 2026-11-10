// Paso 3 de la reserva: muestra los horarios al elegir una fecha
// y habilita "Continuar" cuando también se elige un horario o turno.
const form = document.getElementById("form-fecha-hora");

if (form) {
  const mensaje = document.getElementById("horarios-vacio");
  const horarios = document.getElementById("horarios");
  const continuar = document.getElementById("btn-continuar");
  const inputFecha = document.getElementById("input-fecha");
  const inputHora = document.getElementById("input-hora");

  form.addEventListener("change", (event) => {
    if (event.target.name === "fecha") {
      mensaje.hidden = true;
      horarios.hidden = false;
      if (inputFecha) inputFecha.value = event.target.value;

      const fechaSeleccionada = event.target.value;
      const turnosItems = horarios.querySelectorAll(".turno-slot");
      turnosItems.forEach((slot) => {
        const slotFecha = slot.getAttribute("data-fecha");
        if (!slotFecha || slotFecha === fechaSeleccionada) {
          slot.hidden = false;
        } else {
          slot.hidden = true;
        }
      });

      horarios.querySelectorAll("input").forEach((input) => { input.checked = false; });
      continuar.disabled = true;
    } else if (event.target.name === "hora" || event.target.name === "turno_id") {
      if (inputHora && event.target.dataset.hora) {
        inputHora.value = event.target.dataset.hora;
      }
      continuar.disabled = false;
    }
  });
}
