from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from app.services import turno_service

patient_bp = Blueprint("patient", __name__)

DIAS_SEMANA = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo"
}

MESES = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre"
}

MAPA_DIAS = {
    "0": 0, "1": 0, "lunes": 0,
    "2": 1, "martes": 1,
    "3": 2, "miercoles": 2, "miércoles": 2,
    "4": 3, "jueves": 3,
    "5": 4, "viernes": 4,
    "6": 5, "sabado": 5, "sábado": 5,
    "7": 6, "domingo": 6,
}


@patient_bp.route("/pacientes", methods=["GET", "POST"])
def patient_home():
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para acceder al panel de pacientes.", "error")
        return redirect(url_for("auth.mostrar_login"))

    proximo_turno = None
    try:
        turnos = turno_service.listar_mis_turnos(token)
        proximos = [t for t in turnos if t["estado"] in ("reservado", "confirmado")]
        if proximos:
            proximo_turno = proximos[0]
    except RuntimeError:
        pass

    try:
        especialidades = turno_service.listar_especialidades(token)
        medicos_raw = turno_service.listar_medicos(token)
    except RuntimeError:
        especialidades = []
        medicos_raw = []

    medicos = []
    for m in medicos_raw:
        nom = m.get("nombre", "")
        ape = m.get("apellido", "")
        inits = f"{nom[:1]}{ape[:1]}".upper() if nom and ape else "MD"
        m_id = m.get("id")
        prefijo = "Dra." if nom.lower().endswith("a") else "Dr."
        nombre_completo = f"{prefijo} {nom} {ape}".strip()

        proxima_disp = "Consultar disponibilidad"
        consultorio_desc = "Consultorio asignado"

        try:
            disponibles = turno_service.obtener_turnos_disponibles(token, m_id)
            futuros = []
            for t in disponibles:
                fh = t.get("fecha_hora")
                if fh:
                    try:
                        dt = datetime.fromisoformat(fh)
                        if dt > datetime.now():
                            futuros.append((dt, t))
                    except ValueError:
                        pass
            if futuros:
                dt_prox, t_prox = futuros[0]
                dia_nom = DIAS_SEMANA.get(dt_prox.weekday(), "")
                mes_nom = MESES.get(dt_prox.month, "")
                proxima_disp = f"{dia_nom} {dt_prox.day} de {mes_nom} · {dt_prox.strftime('%H:%M')}"
                sala = t_prox.get("consultorio_sala", "")
                piso = t_prox.get("consultorio_piso", "")
                consultorio_desc = f"Consultorio {sala}" + (f" · Piso {piso}" if piso else "")
        except RuntimeError:
            pass

        medicos.append({
            "id": m_id,
            "nombre": nom,
            "apellido": ape,
            "nombre_completo": nombre_completo,
            "iniciales": inits,
            "especialidad": m.get("especialidad", ""),
            "especialidad_id": m.get("especialidad_id"),
            "email": m.get("email", ""),
            "proxima_disponibilidad": proxima_disp,
            "consultorio": consultorio_desc
        })

    especialidad_filtro = request.args.get("especialidad", "").strip()
    medico_filtro = (request.args.get("medico_id") or request.args.get("q", "")).strip()
    dia_filtro = request.args.get("dia", "").strip()
    buscar_param = request.args.get("buscar")

    busqueda_realizada = bool(buscar_param or especialidad_filtro or medico_filtro or dia_filtro)
    turnos_busqueda = []

    if busqueda_realizada:
        medicos_consulta = medicos
        if medico_filtro:
            try:
                m_id_int = int(medico_filtro)
                medicos_consulta = [m for m in medicos if m["id"] == m_id_int]
            except ValueError:
                medicos_consulta = [
                    m for m in medicos
                    if medico_filtro.lower() in m["apellido"].lower() or medico_filtro.lower() in m["nombre"].lower()
                ]
        elif especialidad_filtro:
            try:
                esp_id_int = int(especialidad_filtro)
                medicos_consulta = [m for m in medicos if m.get("especialidad_id") == esp_id_int]
            except ValueError:
                pass

        dia_objetivo = MAPA_DIAS.get(dia_filtro.lower()) if dia_filtro else None

        for med in medicos_consulta:
            try:
                disponibles = turno_service.obtener_turnos_disponibles(token, med["id"])
            except RuntimeError:
                continue

            for t in disponibles:
                fh = t.get("fecha_hora")
                if not fh:
                    continue
                try:
                    dt = datetime.fromisoformat(fh)
                except ValueError:
                    continue

                if dt <= datetime.now():
                    continue

                if dia_objetivo is not None and dt.weekday() != dia_objetivo:
                    continue

                dia_nom = DIAS_SEMANA.get(dt.weekday(), "")
                mes_nom = MESES.get(dt.month, "")
                fecha_str = dt.strftime("%Y-%m-%d")
                hora_str = dt.strftime("%H:%M")
                fecha_form = f"{dia_nom} {dt.day} de {mes_nom}"

                sala = t.get("consultorio_sala", "")
                piso = t.get("consultorio_piso", "")
                consultorio_str = f"Consultorio {sala}" + (f" · Piso {piso}" if piso else "")

                turnos_busqueda.append({
                    "id": t.get("id"),
                    "medico_id": med["id"],
                    "medico": med["nombre_completo"],
                    "iniciales": med["iniciales"],
                    "especialidad": med["especialidad"],
                    "fecha": fecha_str,
                    "fecha_formateada": fecha_form,
                    "hora": hora_str,
                    "consultorio": consultorio_str,
                    "dt": dt
                })

        turnos_busqueda.sort(key=lambda x: x["dt"])

    return render_template(
        "pacientes/home.html",
        proximo_turno=proximo_turno,
        especialidades=especialidades,
        medicos=medicos,
        turnos_busqueda=turnos_busqueda,
        busqueda_realizada=busqueda_realizada,
        filtro_especialidad=especialidad_filtro,
        filtro_medico=medico_filtro,
        filtro_dia=dia_filtro
    )


@patient_bp.route("/mis-turnos", methods=["GET"])
def mis_turnos():
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para ver tus turnos.", "error")
        return redirect(url_for("auth.mostrar_login"))

    try:
        turnos = turno_service.listar_mis_turnos(token)
        proximos = [t for t in turnos if t["estado"] in ("reservado", "confirmado")]
        historial = [t for t in turnos if t["estado"] in ("atendido", "cancelado", "ausente")]
    except RuntimeError as error:
        proximos = []
        historial = []
        flash(str(error), "error")

    return render_template(
        "pacientes/mis_turnos.html",
        proximos=proximos,
        historial=historial
    )


@patient_bp.route("/mis-turnos/<int:turno_id>", methods=["GET"])
def detalle_turno(turno_id: int):
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para ver el detalle del turno.", "error")
        return redirect(url_for("auth.mostrar_login"))

    try:
        turno = turno_service.obtener_detalle_turno(token, turno_id)
    except RuntimeError as error:
        flash(str(error), "error")
        return redirect(url_for("patient.mis_turnos"))

    return render_template("pacientes/detalle_turno.html", turno=turno, turno_id=turno_id)


@patient_bp.route("/qr/<int:turno_id>", methods=["GET"])
def qr_turno(turno_id: int):
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para ver el código QR.", "error")
        return redirect(url_for("auth.mostrar_login"))

    try:
        turno = turno_service.obtener_detalle_turno(token, turno_id)
        qr_data = turno_service.obtener_qr_turno(token, turno_id)
        qr_token = qr_data.get("qr_token")
    except RuntimeError as error:
        flash(str(error), "error")
        return redirect(url_for("patient.mis_turnos"))

    return render_template(
        "pacientes/qr_turno.html",
        turno=turno,
        turno_id=turno_id,
        qr_token=qr_token
    )


@patient_bp.route("/mis-turnos/<int:turno_id>/cancelar", methods=["POST"])
def cancelar_turno_paciente(turno_id: int):
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para cancelar un turno.", "error")
        return redirect(url_for("auth.mostrar_login"))

    try:
        turno_service.cancelar_turno(token, turno_id)
        flash("Turno cancelado exitosamente.", "success")
    except RuntimeError as error:
        flash(str(error), "error")

    return redirect(url_for("patient.mis_turnos"))


@patient_bp.route("/reservar-turno", methods=["GET"])
def reservar_especialidad():
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para reservar un turno.", "error")
        return redirect(url_for("auth.mostrar_login"))

    try:
        especialidades = turno_service.listar_especialidades(token)
    except RuntimeError as error:
        flash(str(error), "error")
        especialidades = []

    return render_template(
        "pacientes/reserva/especialidad.html",
        especialidades=especialidades
    )


@patient_bp.route(
    "/reservar-turno/especialidades/<int:especialidad_id>/medicos",
    methods=["GET"]
)
def reservar_medico(especialidad_id: int):
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para reservar un turno.", "error")
        return redirect(url_for("auth.mostrar_login"))

    try:
        medicos = turno_service.listar_medicos(token, especialidad_id=especialidad_id)
    except RuntimeError as error:
        flash(str(error), "error")
        medicos = []

    return render_template(
        "pacientes/reserva/medico.html",
        especialidad_id=especialidad_id,
        medicos=medicos
    )


@patient_bp.route(
    "/reservar-turno/medicos/<int:medico_id>/fecha-hora",
    methods=["GET"]
)
def reservar_fecha_hora(medico_id: int):
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para reservar un turno.", "error")
        return redirect(url_for("auth.mostrar_login"))

    try:
        medico = turno_service.obtener_medico(token, medico_id)
        turnos_disponibles_raw = turno_service.obtener_turnos_disponibles(token, medico_id)
    except RuntimeError as error:
        flash(str(error), "error")
        medico = {}
        turnos_disponibles_raw = []

    dia_filtro = request.args.get("dia", "").strip()
    dia_objetivo = MAPA_DIAS.get(dia_filtro.lower()) if dia_filtro else None

    fechas_dict = {}
    turnos_lista = []

    for t in turnos_disponibles_raw:
        fecha_hora_str = t.get("fecha_hora")
        if not fecha_hora_str:
            continue
        try:
            dt = datetime.fromisoformat(fecha_hora_str)
        except ValueError:
            continue

        if dt <= datetime.now():
            continue

        if dia_objetivo is not None and dt.weekday() != dia_objetivo:
            continue

        fecha_val = dt.strftime("%Y-%m-%d")
        hora_val = dt.strftime("%H:%M")
        dia_semana_nombre = DIAS_SEMANA.get(dt.weekday(), "")[:3]

        if fecha_val not in fechas_dict:
            fechas_dict[fecha_val] = {
                "valor": fecha_val,
                "dia": dia_semana_nombre,
                "num": dt.day,
                "libres": 0
            }
        fechas_dict[fecha_val]["libres"] += 1

        turnos_lista.append({
            "id": t.get("id"),
            "fecha": fecha_val,
            "hora": hora_val,
            "consultorio": f"Consultorio {t.get('consultorio_sala', '')}"
        })

    fechas = list(fechas_dict.values())

    return render_template(
        "pacientes/reserva/fecha_hora.html",
        medico_id=medico_id,
        medico=medico,
        fechas=fechas,
        turnos_lista=turnos_lista
    )


@patient_bp.route("/reservar-turno/confirmacion", methods=["GET"])
def reservar_confirmacion():
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para confirmar tu turno.", "error")
        return redirect(url_for("auth.mostrar_login"))

    medico_id = request.args.get("medico_id", type=int)
    turno_id = request.args.get("turno_id", type=int)
    fecha = request.args.get("fecha")
    hora = request.args.get("hora")

    if fecha and hora:
        try:
            dt_turno = datetime.fromisoformat(f"{fecha}T{hora}")
            if dt_turno <= datetime.now():
                flash("El turno seleccionado ya ha pasado y no puede ser reservado.", "error")
                if medico_id:
                    return redirect(url_for("patient.reservar_fecha_hora", medico_id=medico_id))
                return redirect(url_for("patient.reservar_especialidad"))
        except Exception:
            pass

    medico = {}
    if medico_id:
        try:
            medico = turno_service.obtener_medico(token, medico_id)
        except RuntimeError:
            pass

    fecha_formateada = None
    if fecha:
        try:
            dt = datetime.fromisoformat(fecha)
            dia_nombre = DIAS_SEMANA.get(dt.weekday(), "")
            mes_nombre = MESES.get(dt.month, "")
            fecha_formateada = f"{dia_nombre} {dt.day} de {mes_nombre}"
        except Exception:
            pass

    return render_template(
        "pacientes/reserva/confirmacion.html",
        medico_id=medico_id,
        turno_id=turno_id,
        medico=medico,
        fecha=fecha,
        fecha_formateada=fecha_formateada,
        hora=hora
    )


@patient_bp.route("/reservar-turno/resultado", methods=["GET", "POST"])
def reservar_resultado():
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para reservar un turno.", "error")
        return redirect(url_for("auth.mostrar_login"))

    turno_id_raw = request.form.get("turno_id") or request.args.get("turno_id")

    if request.method == "POST" and turno_id_raw:
        try:
            turno_id = int(turno_id_raw)
            turno_service.reservar_turno(token, turno_id)
            flash("Turno reservado exitosamente.", "success")
            return redirect(url_for("patient.mis_turnos"))
        except (ValueError, RuntimeError) as error:
            flash(str(error), "error")
            medico_id = request.form.get("medico_id")
            if medico_id:
                return redirect(url_for("patient.reservar_fecha_hora", medico_id=medico_id))
            return redirect(url_for("patient.reservar_especialidad"))

    return render_template(
        "pacientes/reserva/confirmacion.html",
        resultado=True
    )
