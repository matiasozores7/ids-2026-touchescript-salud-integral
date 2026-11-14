document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("coberturas-buscar");
    const tabla = document.getElementById("coberturas-tabla");
    const contador = document.getElementById("coberturas-contador");
    const mensajeVacio = document.getElementById("coberturas-vacio");

    if (!input || !tabla || !contador || !mensajeVacio) {
        console.error("No se encontraron los elementos del listado de coberturas.");
        return;
    }

    const filas = Array.from(
        tabla.querySelectorAll("tbody tr[data-busqueda]")
    );

    input.addEventListener("input", () => {
        const busqueda = input.value.trim().toLowerCase();
        let coincidencias = 0;

        filas.forEach((fila) => {
            const nombre = fila.dataset.busqueda;
            const coincide = nombre.includes(busqueda);

            fila.hidden = !coincide;

            if (coincide) {
                coincidencias++;
            }
        });

        contador.textContent = coincidencias;
        mensajeVacio.hidden = coincidencias > 0 || filas.length === 0;
    });


    const modal = document.getElementById("cobertura-modal");
    const formulario = document.getElementById("cobertura-form");
    const titulo = document.getElementById("cobertura-modal-titulo");
    const nombreInput = document.getElementById("cobertura-nombre");
    const botonGuardar = document.getElementById("cobertura-guardar");

    if (modal && formulario && titulo && nombreInput && botonGuardar) {
        modal.addEventListener("show.bs.modal", (event) => {
            const boton = event.relatedTarget;
            const accion = boton?.dataset.accion;

            if (accion === "editar") {
                const fila = boton.closest("tr");
                const coberturaId = fila.dataset.id;

                titulo.textContent = "Editar cobertura";
                nombreInput.value = fila.dataset.nombre;
                formulario.action = formulario.dataset.urlEditar.replace(
                    "/0/editar",
                    `/${coberturaId}/editar`
                );
                botonGuardar.textContent = "Guardar cambios";
            } else {
                titulo.textContent = "Nueva cobertura";
                nombreInput.value = "";
                formulario.action = formulario.dataset.urlEditar.replace(
                    /coberturas\/0\/editar$/,
                    "coberturas/nueva"
                );
                botonGuardar.textContent = "Guardar cobertura";
            }
        });
    }

    const modalEliminar = document.getElementById("eliminar-cobertura-modal");
    const formularioEliminar = document.getElementById("eliminar-cobertura-form");
    const nombreEliminar = document.getElementById("eliminar-cobertura-nombre");

    if (modalEliminar && formularioEliminar && nombreEliminar) {
        modalEliminar.addEventListener("show.bs.modal", (event) => {
            const boton = event.relatedTarget;

            formularioEliminar.action = boton.dataset.urlEliminar;
            nombreEliminar.textContent = boton.dataset.nombre;
        });
    }

});