
document.addEventListener("DOMContentLoaded", function () {

    function actualizarTiempos() {
        const elementos = document.querySelectorAll("[data-turno]");

        elementos.forEach(function (elemento) {

            const turno = new Date(elemento.dataset.turno);
            const ahora = new Date();

            // Calcula los minutos transcurridos desde la hora del turno.
            const minutos = Math.max(
                0,
                Math.floor((ahora - turno) / 60000)
            );

            let estado = "En horario";

            if (minutos > 0) {
                estado = "Demorado";
            }

            // Actualiza el texto.
            elemento.textContent = `${minutos} min · ${estado}`;

            // Aplica el estilo cuando existe demora.
            elemento.classList.toggle(
                "sala-tiempo-demorado",
                minutos > 0
            );

        });
    }

    // Ejecuta el cálculo al cargar la página.
    actualizarTiempos();

    // Actualiza cada minuto.
    setInterval(actualizarTiempos, 60000);

});
