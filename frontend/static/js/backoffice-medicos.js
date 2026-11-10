/* Listado de médicos del backoffice.
   - Filtra la tabla mientras se escribe en el buscador.
   - Completa los modales (alta/edición y baja) con los datos de la fila,
     usando el evento show.bs.modal de Bootstrap (relatedTarget = botón que lo abrió). */

(() => {
  const filas = document.querySelectorAll("#medicos-tabla tbody tr");
  const buscador = document.querySelector("#medicos-buscar");
  const contador = document.querySelector("#medicos-contador");
  const vacio = document.querySelector("#medicos-vacio");

  buscador?.addEventListener("input", () => {
    const consulta = buscador.value.trim().toLowerCase();
    let visibles = 0;

    filas.forEach((fila) => {
      const coincide = fila.dataset.busqueda.includes(consulta);
      fila.hidden = !coincide;
      if (coincide) visibles += 1;
    });

    contador.textContent = visibles;
    vacio.hidden = visibles > 0;
  });

  // Los botones de cada fila guardan el médico completo en data-medico (JSON).
  const leerMedico = (evento) => {
    const datos = evento.relatedTarget?.dataset.medico;
    return datos ? JSON.parse(datos) : null;
  };

  const modalFormulario = document.querySelector("#medico-modal");

  modalFormulario?.addEventListener("show.bs.modal", (evento) => {
    const medico = leerMedico(evento);
    const formulario = modalFormulario.querySelector("form");

    formulario.reset(); // vuelve a los valores por defecto (alta)
    // reset() no limpia los inputs ocultos, por eso el id se asigna siempre a mano
    formulario.elements.id.value = medico?.id ?? "";
    modalFormulario.querySelector(".modal-title").textContent = medico ? "Editar médico" : "Nuevo médico";

    // La contraseña solo se pide al crear: el PATCH no la modifica.
    modalFormulario.querySelectorAll("[data-solo-alta]").forEach((bloque) => {
      bloque.hidden = Boolean(medico);
      bloque.querySelectorAll("input").forEach((campo) => { campo.disabled = Boolean(medico); });
    });

    if (!medico) return;

    ["titulo", "matricula", "nombre", "apellido", "especialidad_id", "consultorio_id",
     "email", "telefono", "experiencia", "presentacion"].forEach((campo) => {
      formulario.elements[campo].value = medico[campo] ?? "";
    });
    formulario.elements.activo.checked = medico.activo ?? true;
    formulario.querySelectorAll('[name="coberturas"]').forEach((casilla) => {
      casilla.checked = (medico.coberturas ?? []).includes(Number(casilla.value));
    });
  });

  const modalBaja = document.querySelector("#medico-baja-modal");

  modalBaja?.addEventListener("show.bs.modal", (evento) => {
    const medico = leerMedico(evento);
    if (!medico) return;

    modalBaja.querySelector("[data-medico-nombre]").textContent = medico.nombre_completo;
    modalBaja.querySelector('input[name="id"]').value = medico.id;
  });
})();
