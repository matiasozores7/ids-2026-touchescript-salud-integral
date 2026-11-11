from flask import render_template, request, flash, redirect, url_for

from . import backoffice_bp
from app.services import checkin_service
from app.errors.exceptions import AppError


@backoffice_bp.route("/backoffice/check-in", methods=["GET", "POST"])
def backoffice_checkin():
    if request.method == "POST":
        qr_token = request.form.get("qr_token", "").strip()

        if not qr_token:
            flash("Ingresá el código QR del comprobante.", "error")
            return redirect(url_for("backoffice.backoffice_checkin"))

        try:
            checkin_service.realizar_checkin(qr_token)
            flash(
                "Check-in registrado correctamente. El paciente ingresó a la sala de espera.",
                "success"
            )

        except AppError as error:
            flash(error.message, "error")

        return redirect(url_for("backoffice.backoffice_checkin"))

    return render_template("recepcion/checkin.html")