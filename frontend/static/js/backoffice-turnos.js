/* Funcionalidad del listado de turnos. */

(() => {
    const filas = document.querySelectorAll(
        "#turnos-tabla tbody tr[data-busqueda]"
    );

    const buscador = document.querySelector("#turnos-buscar");
    const contador = document.querySelector("#turnos-contador");
    const vacio = document.querySelector("#turnos-vacio");

    if (!buscador) return;

    buscador.addEventListener("input", () => {
        const consulta = buscador.value.trim().toLowerCase();
        let visibles = 0;

        filas.forEach((fila) => {
            const coincide = fila.dataset.busqueda.includes(consulta);

            fila.hidden = !coincide;

            if (coincide) visibles++;
        });

        if (contador) {
            contador.textContent = visibles;
        }

        if (vacio) {
            vacio.hidden = visibles !== 0;
        }
    });
})();