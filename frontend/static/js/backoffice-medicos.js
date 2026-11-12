
/* Funcionalidad del listado y los formularios de médicos. */

(() => {
    const filas = document.querySelectorAll("#medicos-tabla tbody tr");
    const buscador = document.querySelector("#medicos-buscar");
    const contador = document.querySelector("#medicos-contador");
    const vacio = document.querySelector("#medicos-vacio");

    // Búsqueda de médicos en la tabla.
    buscador?.addEventListener("input", () => {
        const consulta = buscador.value.trim().toLowerCase();
        let visibles = 0;

        filas.forEach((fila) => {
            const coincide = (fila.dataset.busqueda || "").includes(consulta);

            fila.hidden = !coincide;

            if (coincide) {
                visibles += 1;
            }
        });

        if (contador) contador.textContent = visibles;
        if (vacio) vacio.hidden = visibles > 0;
    });

    // Recupera los datos del médico guardados en el botón.
    const leerMedico = (evento) => {
        const datos = evento.relatedTarget?.dataset.medico;

        return datos ? JSON.parse(datos) : null;
    };

    // Modal de alta y edición.
    const modalFormulario = document.querySelector("#medico-modal");

    modalFormulario?.addEventListener("show.bs.modal", (evento) => {
        const medico = leerMedico(evento);
        const formulario = document.querySelector("#medico-form");

        formulario.reset();

        const esEdicion = Boolean(medico);

        modalFormulario.querySelector(".modal-title").textContent =
            esEdicion ? "Editar médico" : "Nuevo médico";

        // Configura la ruta según la operación.
        formulario.action = esEdicion
            ? `/backoffice/medicos/${medico.id}/editar`
            : "/backoffice/medicos";

        // La contraseña solamente se solicita al crear.
        modalFormulario.querySelectorAll("[data-solo-alta]").forEach((bloque) => {
            bloque.hidden = esEdicion;

            bloque.querySelectorAll("input").forEach((campo) => {
                campo.disabled = esEdicion;
            });
        });

        if (!medico) return;

        // Completa los campos con los datos existentes.
        [
            "matricula",
            "nombre",
            "apellido",
            "especialidad_id",
            "email",
            "telefono"
        ].forEach((campo) => {
            formulario.elements[campo].value = medico[campo] ?? "";
        });

        // Las coberturas del médico vienen como objetos:
        // [{id: 1, nombre: "OSDE"}, ...]
        const coberturasIds = (medico.coberturas ?? []).map(
            (cobertura) => Number(cobertura.id)
        );

        formulario.querySelectorAll('[name="coberturas"]').forEach((casilla) => {
            casilla.checked = coberturasIds.includes(Number(casilla.value));
        });
    });

    // Modal de baja lógica.
    const modalBaja = document.querySelector("#medico-baja-modal");

    modalBaja?.addEventListener("show.bs.modal", (evento) => {
        const medico = leerMedico(evento);

        if (!medico) return;

        modalBaja.querySelector("[data-medico-nombre]").textContent =
            `${medico.nombre} ${medico.apellido}`;

        modalBaja.querySelector("#medico-baja-form").action =
            `/backoffice/medicos/${medico.id}/eliminar`;
    });
})();
