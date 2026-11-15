
document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("qr-code");

    if (!container) {
        return;
    }

    const token = container.dataset.qrToken;

    if (!token) {
        container.textContent = "No se encontró el token del turno.";
        return;
    }

    if (typeof QRCode === "undefined") {
        container.textContent = "No se pudo cargar el generador del QR.";
        return;
    }

    new QRCode(container, {
        text: token,
        width: 188,
        height: 188,
        correctLevel: QRCode.CorrectLevel.H
    });
});
