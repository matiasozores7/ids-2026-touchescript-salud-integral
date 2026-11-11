document.addEventListener("DOMContentLoaded", function () {
    const notificaciones = document.querySelectorAll("[data-toast]");

    notificaciones.forEach(function (elemento) {
        const toast = new bootstrap.Toast(elemento, {
            autohide: true,
            delay: 5000
        });

        toast.show();
    });
});