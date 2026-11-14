
/* Funcionalidad del listado de turnos. */

(() => {
    const filas = document.querySelectorAll(
        "#turnos-tabla tbody tr[data-busqueda]"
    );

    const buscador = document.querySelector("#turnos-buscar");
    const contador = document.querySelector("#turnos-contador");
    const vacio = document.querySelector("#turnos-vacio");

    // Búsqueda local de turnos.
    buscador?.addEventListener("input", () => {
        const consulta = buscador.value.trim().toLowerCase();
        let visibles = 0;

        filas.forEach((fila) => {
            const coincide = (fila.dataset.busqueda || "")
                .includes(consulta);

            fila.hidden = !coincide;

            if (coincide) {
                visibles += 1;
            }
        });

        // Actualiza el contador de resultados.
        if (contador) {
            contador.textContent = visibles;
        }

        // Muestra u oculta el mensaje de búsqueda sin resultados.
        if (vacio) {
            vacio.hidden = visibles > 0;
        }
    });
})();
