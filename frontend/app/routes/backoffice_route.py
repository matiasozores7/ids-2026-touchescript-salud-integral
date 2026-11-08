from flask import Blueprint, redirect, render_template, request, session, url_for

from app.services import consultorio_service


backoffice_bp = Blueprint("backoffice", __name__)


def _render_consultorios(error: str | None = None):
    try:
        consultorios = consultorio_service.listar_consultorios()
    except RuntimeError as exc:
        return render_template(
            "backoffice/consultorios.html",
            consultorios=[],
            error=str(exc),
        )

    return render_template(
        "backoffice/consultorios.html",
        consultorios=consultorios,
        error=error,
    )


@backoffice_bp.get("/backoffice/consultorios")
def backoffice_consultorios():
    if not session.get("access_token"):
        return redirect(url_for("auth.mostrar_login"))
    return _render_consultorios()


@backoffice_bp.route(
    "/backoffice/consultorios/nuevo",
    methods=["GET", "POST"],
)
@backoffice_bp.route(
    "/backoffice/consultorios/<int:consultorio_id>/editar",
    methods=["GET", "POST"],
)
def backoffice_consultorio_form(consultorio_id: int | None = None):
    if not session.get("access_token"):
        return redirect(url_for("auth.mostrar_login"))

    consultorio = None
    if consultorio_id is not None:
        try:
            consultorio = next(
                (
                    item
                    for item in consultorio_service.listar_consultorios()
                    if item.get("id") == consultorio_id
                ),
                None,
            )
        except RuntimeError as exc:
            return render_template(
                "backoffice/consultorio_form.html",
                consultorio=None,
                error=str(exc),
            )

        if consultorio is None:
            return redirect(url_for("backoffice.backoffice_consultorios"))

    if request.method == "POST":
        numero_sala = request.form.get("numero_sala", "").strip()
        piso = request.form.get("piso", "").strip()

        try:
            if consultorio_id is None:
                consultorio_service.crear_consultorio(numero_sala, piso)
            else:
                consultorio_service.actualizar_consultorio(
                    consultorio_id,
                    numero_sala,
                    piso,
                )
        except RuntimeError as exc:
            return render_template(
                "backoffice/consultorio_form.html",
                consultorio=consultorio,
                error=str(exc),
            )

        return redirect(url_for("backoffice.backoffice_consultorios"))

    return render_template(
        "backoffice/consultorio_form.html",
        consultorio=consultorio,
        error=None,
    )


@backoffice_bp.post("/backoffice/consultorios/<int:consultorio_id>/eliminar")
def eliminar_consultorio(consultorio_id: int):
    if not session.get("access_token"):
        return redirect(url_for("auth.mostrar_login"))

    try:
        consultorio_service.eliminar_consultorio(consultorio_id)
        return redirect(url_for("backoffice.backoffice_consultorios"))
    except RuntimeError as exc:
        return _render_consultorios(error=str(exc))
