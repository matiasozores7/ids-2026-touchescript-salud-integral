from flask import render_template, request, url_for

from app.services.turnos_service import (
    listar_turnos_administrativos,
    listar_medicos,
    listar_especialidades
)
from app.routes.backoffice import backoffice_bp


@backoffice_bp.route("/turnos")
def backoffice_turnos():

    limit = request.args.get("_limit", 10, type=int)
    offset = request.args.get("_offset", 0, type=int)

    filtros = {
        "fecha": request.args.get("fecha") or None,
        "estado": request.args.get("estado") or None,
        "especialidad_id": request.args.get("especialidad_id") or None,
        "medico_id": request.args.get("medico_id") or None,
        "busqueda": request.args.get("busqueda", "").strip() or None
    }

    resultado = listar_turnos_administrativos(
        limit=limit,
        offset=offset,
        **filtros
    )

    medicos = listar_medicos()
    especialidades = listar_especialidades()

    def url_pagina(nuevo_offset):
        parametros = request.args.to_dict()
        parametros["_limit"] = limit
        parametros["_offset"] = nuevo_offset

        return url_for(
            "backoffice.backoffice_turnos",
            **parametros
        )

    total = resultado["total"]

    paginacion = {
        "anterior": url_pagina(max(0, offset - limit)) if offset > 0 else None,
        "siguiente": url_pagina(offset + limit)
        if offset + limit < total else None
    }

    return render_template(
        "backoffice/turnos.html",
        turnos=resultado["items"],
        total=total,
        medicos=medicos,
        especialidades=especialidades,
        paginacion=paginacion,
        limit=limit,
        offset=offset
    )