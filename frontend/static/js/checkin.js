
document.addEventListener("DOMContentLoaded", () => {
    const scannerContainer = document.getElementById("qr-reader");
    const startButton = document.getElementById("start-scanner");
    const stopButton = document.getElementById("stop-scanner");
    const status = document.getElementById("scanner-status");
    const tokenInput = document.getElementById("qr_token");
    const form = document.querySelector(".checkin-code-form");

    const scanner = new Html5Qrcode("qr-reader");

    let scannerActivo = false;
    let procesando = false;

    async function iniciarEscaner() {
        try {
            await scanner.start(
                { facingMode: "environment" },
                {
                    fps: 10,
                    qrbox: { width: 250, height: 250 }
                },
                async (decodedText) => {
                    if (procesando) return;

                    procesando = true;

                    // Detener la cámara antes de enviar el formulario.
                    await detenerEscaner();

                    tokenInput.value = decodedText;
                    form.submit();
                },
                () => {
                    // No hacer nada mientras busca un código QR.
                }
            );

            scannerActivo = true;
            startButton.hidden = true;
            stopButton.hidden = false;
            status.textContent = "Cámara activa. Enfocá el código QR.";

        } catch (error) {
            status.textContent =
                "No se pudo acceder a la cámara. Verificá los permisos del navegador.";

            console.error("Error al iniciar el escáner:", error);
        }
    }

    async function detenerEscaner() {
        if (!scannerActivo) return;

        try {
            await scanner.stop();
            scannerActivo = false;

            startButton.hidden = false;
            stopButton.hidden = true;

        } catch (error) {
            console.error("Error al detener el escáner:", error);
        }
    }

    startButton.addEventListener("click", iniciarEscaner);
    stopButton.addEventListener("click", detenerEscaner);
});
