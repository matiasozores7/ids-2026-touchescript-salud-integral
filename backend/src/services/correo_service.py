import logging
import smtplib
import ssl
import struct
import zlib
from datetime import datetime
from email.message import EmailMessage
from html import escape
from urllib.parse import urlencode

import qrcode
from flask import current_app
from pymysql import MySQLError

from src.database.connection import get_db_connection
from src.repositories import turno_repository as turno_repo
from src.services.turno_service import generar_token_cancelacion


_DIAS = (
    "lunes",
    "martes",
    "miércoles",
    "jueves",
    "viernes",
    "sábado",
    "domingo",
)
_MESES = (
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
)
_LOGGER = logging.getLogger(__name__)


def _formatear_fecha_hora(valor) -> tuple[str, str]:
    fecha_hora = (
        datetime.fromisoformat(valor) if isinstance(valor, str) else valor
    )
    if not isinstance(fecha_hora, datetime):
        raise ValueError("La fecha y hora del turno no son válidas.")

    fecha = (
        f"{_DIAS[fecha_hora.weekday()]} {fecha_hora.day} "
        f"de {_MESES[fecha_hora.month - 1]} de {fecha_hora.year}"
    )
    return fecha, fecha_hora.strftime("%H:%M")


def _crear_chunk_png(tipo: bytes, contenido: bytes) -> bytes:
    datos = tipo + contenido
    return (
        struct.pack(">I", len(contenido))
        + datos
        + struct.pack(">I", zlib.crc32(datos) & 0xFFFFFFFF)
    )


def _generar_qr_png(valor: str) -> bytes:
    codigo = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=1,
        border=4,
    )
    codigo.add_data(valor)
    codigo.make(fit=True)

    matriz = codigo.get_matrix()
    escala = 5
    ancho = len(matriz) * escala
    filas = bytearray()

    for fila in matriz:
        for _ in range(escala):
            filas.append(0)
            for modulo in fila:
                filas.extend(bytes((0 if modulo else 255,)) * escala)

    encabezado = struct.pack(">IIBBBBB", ancho, ancho, 8, 0, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + _crear_chunk_png(b"IHDR", encabezado)
        + _crear_chunk_png(b"IDAT", zlib.compress(bytes(filas)))
        + _crear_chunk_png(b"IEND", b"")
    )


def generar_plantilla_reserva(
    datos_turno: dict,
    url_cancelar: str,
    url_portal: str,
) -> tuple[str, str]:
    fecha, hora = _formatear_fecha_hora(datos_turno["fecha_hora"])
    paciente = " ".join(
        parte
        for parte in (
            datos_turno.get("paciente_nombre"),
            datos_turno.get("paciente_apellido"),
        )
        if parte
    ) or "Paciente"
    medico = " ".join(
        parte
        for parte in (
            datos_turno.get("medico_nombre"),
            datos_turno.get("medico_apellido"),
        )
        if parte
    ) or "Profesional asignado"
    especialidad = datos_turno.get("especialidad_nombre") or "Consulta médica"
    sala = datos_turno.get("consultorio_sala") or "Sin asignar"
    piso = datos_turno.get("consultorio_piso")
    consultorio = f"Consultorio {sala}"
    if piso is not None:
        consultorio += f", piso {piso}"

    valores_html = {
        "paciente": escape(paciente, quote=True),
        "medico": escape(f"Dr. {medico}", quote=True),
        "especialidad": escape(str(especialidad), quote=True),
        "fecha": escape(fecha, quote=True),
        "hora": escape(hora, quote=True),
        "consultorio": escape(str(consultorio), quote=True),
        "url_cancelar": escape(url_cancelar, quote=True),
        "url_portal": escape(url_portal, quote=True),
    }

    texto = f"""Hola {paciente}:

Tu turno en Salud Integral quedó reservado.

Profesional: Dr. {medico}
Especialidad: {especialidad}
Fecha: {fecha}
Hora: {hora}
Consultorio: {consultorio}

El QR adjunto contiene el código de tu turno. Presentalo al llegar.

Cancelar la reserva: {url_cancelar}
Ver mis turnos: {url_portal}
"""

    html = f"""<!doctype html>
<html lang="es">
  <body style="margin:0;background:#f7f9fa;color:#354052;font-family:Arial,sans-serif">
    <main style="box-sizing:border-box;max-width:580px;margin:24px auto;padding:28px;background:#fff;border:1px solid #e3e8ec;border-radius:14px">
      <header style="padding:18px 22px;background:#294d5d;color:#fff;border-radius:10px">
        <strong style="font-size:20px">Salud Integral</strong><br>
        <span style="font-size:12px">CENTRO MÉDICO</span>
      </header>
      <h1 style="color:#294d5d;font-size:23px;margin:24px 0 8px">Tu turno está reservado</h1>
      <p>Hola <strong>{valores_html["paciente"]}</strong>, estos son los datos de tu turno:</p>
      <table role="presentation" style="width:100%;padding:16px;background:#f7f9fa;border-radius:10px">
        <tr><td><strong>Profesional:</strong> {valores_html["medico"]}</td></tr>
        <tr><td><strong>Especialidad:</strong> {valores_html["especialidad"]}</td></tr>
        <tr><td><strong>Fecha:</strong> {valores_html["fecha"]}</td></tr>
        <tr><td><strong>Hora:</strong> {valores_html["hora"]}</td></tr>
        <tr><td><strong>Consultorio:</strong> {valores_html["consultorio"]}</td></tr>
      </table>
      <h2 style="color:#294d5d;font-size:17px;margin:24px 0 8px">Código QR del turno</h2>
      <p>Presentá este código al llegar al centro médico.</p>
      <p style="text-align:center"><img src="cid:turno-qr" alt="Código QR del turno" width="220" height="220"></p>
      <p style="text-align:center;margin:24px 0">
        <a href="{valores_html["url_cancelar"]}" style="display:inline-block;padding:13px 22px;background:#b42332;color:#fff;text-decoration:none;border-radius:8px;font-weight:bold">Cancelar reserva</a>
      </p>
      <p style="text-align:center">
        <a href="{valores_html["url_portal"]}" style="color:#477f9a">Ver mis turnos</a>
      </p>
      <footer style="margin-top:24px;color:#788493;font-size:12px;text-align:center">
        Si no podés asistir, cancelá con anticipación para liberar el horario.
      </footer>
    </main>
  </body>
</html>"""

    return html, texto


def enviar_correo(
    destinatario: str,
    asunto: str,
    cuerpo_html: str,
    cuerpo_texto: str,
    qr_png: bytes,
) -> bool:
    try:
        config = current_app.config
        smtp_host = config["SMTP_HOST"]
        smtp_port = config["SMTP_PORT"]
        smtp_user = config["SMTP_USER"]
        smtp_password = config["SMTP_PASSWORD"]
        smtp_tls = config["SMTP_TLS"]
        smtp_ssl = config["SMTP_SSL"]

        if smtp_tls and smtp_ssl:
            raise ValueError("SMTP_TLS y SMTP_SSL no pueden estar activos a la vez.")
        if bool(smtp_user) != bool(smtp_password):
            raise ValueError("SMTP_USER y SMTP_PASSWORD deben configurarse juntos.")

        mensaje = EmailMessage()
        mensaje["Subject"] = asunto
        mensaje["From"] = config["EMAIL_REMITENTE"]
        mensaje["To"] = destinatario
        mensaje.set_content(cuerpo_texto)
        mensaje.add_alternative(cuerpo_html, subtype="html")
        cuerpo_html_mime = mensaje.get_body(preferencelist=("html",))
        cuerpo_html_mime.add_related(
            qr_png,
            maintype="image",
            subtype="png",
            cid="<turno-qr>",
            filename="codigo-turno.png",
            disposition="inline",
        )

        contexto_ssl = ssl.create_default_context()
        if smtp_ssl:
            servidor = smtplib.SMTP_SSL(
                smtp_host,
                smtp_port,
                timeout=10,
                context=contexto_ssl,
            )
        else:
            servidor = smtplib.SMTP(smtp_host, smtp_port, timeout=10)

        with servidor:
            if smtp_tls:
                servidor.starttls(context=contexto_ssl)
            if smtp_user:
                servidor.login(smtp_user, smtp_password)
            servidor.send_message(mensaje)

    except (OSError, smtplib.SMTPException, ValueError):
        _LOGGER.exception("No se pudo enviar el correo de reserva.")
        return False

    return True


def enviar_aviso_reserva(turno_id: int) -> bool:
    try:
        connection = get_db_connection()
        try:
            datos_turno = turno_repo.obtener_turno_con_detalles_para_correo(
                connection,
                turno_id,
            )
        finally:
            connection.close()
    except MySQLError:
        _LOGGER.exception(
            "No se pudieron cargar los datos del turno %s para enviar el correo.",
            turno_id,
        )
        return False

    if not datos_turno:
        _LOGGER.error("No se encontraron datos para enviar el turno %s.", turno_id)
        return False

    destinatario = datos_turno.get("paciente_email")
    qr_token = datos_turno.get("qr_token")
    if not destinatario or not qr_token:
        _LOGGER.error(
            "El turno %s no tiene correo de paciente o token QR.",
            turno_id,
        )
        return False

    try:
        cancel_token = generar_token_cancelacion(turno_id, qr_token)
    except RuntimeError:
        _LOGGER.exception(
            "No se pudo generar el enlace de cancelación para el turno %s.",
            turno_id,
        )
        return False
    frontend_url = current_app.config["FRONTEND_URL"].rstrip("/")
    url_cancelar = (
        f"{frontend_url}/cancelar-reserva?"
        + urlencode({"turno_id": turno_id, "token": cancel_token})
    )
    url_portal = f"{frontend_url}/mis-turnos/{turno_id}"
    cuerpo_html, cuerpo_texto = generar_plantilla_reserva(
        datos_turno,
        url_cancelar,
        url_portal,
    )

    qr_png = _generar_qr_png(qr_token)
    return enviar_correo(
        destinatario=destinatario,
        asunto="Confirmación de tu turno - Salud Integral",
        cuerpo_html=cuerpo_html,
        cuerpo_texto=cuerpo_texto,
        qr_png=qr_png,
    )
