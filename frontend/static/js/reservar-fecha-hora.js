// Paso 3 de la reserva: muestra los horarios al elegir una fecha
// y habilita "Continuar" cuando también se elige un horario.
const form = document.getElementById("form-fecha-hora");

if (form) {
  const mensaje = document.getElementById("horarios-vacio");
  const horarios = document.getElementById("horarios");
  const continuar = document.getElementById("btn-continuar");

  form.addEventListener("change", (event) => {
    if (event.target.name === "fecha") {
      mensaje.hidden = true;
      horarios.hidden = false;
      horarios.querySelectorAll("input").forEach((input) => { input.checked = false; });
      continuar.disabled = true;
    } else if (event.target.name === "hora") {
      continuar.disabled = false;
    }
  });
}
