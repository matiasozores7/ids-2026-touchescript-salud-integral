import os
import smtplib
import logging
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.database.connection import get_db_connection
from src.repositories import turno_repository as turno_repo

DIAS_SEMANA = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo",
}

MESES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}


def _formatear_fecha_hora(fecha_hora_val) -> tuple[str, str]:
    if isinstance(fecha_hora_val, str):
        try:
            fecha_hora_val = datetime.fromisoformat(fecha_hora_val)
        except Exception:
            return str(fecha_hora_val), ""

    if isinstance(fecha_hora_val, datetime):
        dia_nom = DIAS_SEMANA.get(fecha_hora_val.weekday(), "")
        mes_nom = MESES.get(fecha_hora_val.month, "")
        fecha_texto = f"{dia_nom} {fecha_hora_val.day} de {mes_nom} de {fecha_hora_val.year}"
        hora_texto = fecha_hora_val.strftime("%H:%M hs")
        return fecha_texto, hora_texto

    return str(fecha_hora_val), ""


def generar_plantilla_reserva(
    datos_turno: dict,
    url_cancelar: str,
    url_portal: str
) -> tuple[str, str]:
    paciente_nombre = datos_turno.get("paciente_nombre") or "Paciente"
    paciente_apellido = datos_turno.get("paciente_apellido") or ""
    paciente_completo = f"{paciente_nombre} {paciente_apellido}".strip()

    medico_nombre = datos_turno.get("medico_nombre") or ""
    medico_apellido = datos_turno.get("medico_apellido") or ""
    medico_completo = f"Dr. {medico_nombre} {medico_apellido}".strip()

    especialidad = datos_turno.get("especialidad_nombre") or "Consulta médica"
    sala = datos_turno.get("consultorio_sala") or "Sin asignar"
    piso = datos_turno.get("consultorio_piso") or "PB"
    consultorio_texto = f"Consultorio {sala} (Piso {piso})"

    fecha_texto, hora_texto = _formatear_fecha_hora(datos_turno.get("fecha_hora"))
    turno_id = datos_turno.get("id", "")

    # Versión texto plano
    cuerpo_texto = f"""¡Hola {paciente_completo}!

Confirmamos la reserva de tu turno en Salud Integral.

Detalle del turno #{turno_id}:
- Especialidad: {especialidad}
- Profesional: {medico_completo}
- Fecha: {fecha_texto}
- Horario: {hora_texto}
- Ubicación: {consultorio_texto}

Para cancelar esta reserva, hacé clic en el siguiente enlace:
{url_cancelar}

Para ver el turno en el portal de pacientes:
{url_portal}

Recordá presentarte 10 minutos antes del horario asignado.
Salud Integral · Centro Médico
"""

    # Versión HTML acorde a la identidad visual de la web (#477f9a, #294d5d, #4ca7a1, #f7f9fa, #eaf3f7)
    cuerpo_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Reserva de Turno · Salud Integral</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f7f9fa; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #354052; -webkit-font-smoothing: antialiased;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f7f9fa; padding: 30px 10px;">
    <tr>
      <td align="center">
        <!-- Contenedor principal -->
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width: 580px; background-color: #ffffff; border-radius: 14px; border: 1px solid #e3e8ec; overflow: hidden; box-shadow: 0 4px 14px rgba(41, 77, 93, 0.06);">
          
          <!-- Encabezado con Identidad de Marca -->
          <tr>
            <td style="background: linear-gradient(135deg, #294d5d 0%, #477f9a 100%); padding: 28px 32px; text-align: left;">
              <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                <tr>
                  <td>
                    <!-- Isotipo estilizado -->
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0">
                      <tr>
                        <td style="width: 38px; height: 38px; background-color: #eaf3f7; border-radius: 50%; text-align: center; vertical-align: middle; border: 2px solid #477f9a;">
                          <span style="color: #4ca7a1; font-size: 22px; font-weight: 800; line-height: 1; display: inline-block;">+</span>
                        </td>
                        <td style="padding-left: 12px;">
                          <div style="color: #ffffff; font-size: 20px; font-weight: 800; letter-spacing: -0.3px; line-height: 1.1;">Salud Integral</div>
                          <div style="color: #eaf3f7; font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 2px;">Centro Médico</div>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Cuerpo del correo -->
          <tr>
            <td style="padding: 32px 32px 24px 32px;">
              
              <!-- Badge de estado -->
              <div style="display: inline-block; background-color: #eaf3f7; color: #477f9a; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; padding: 6px 12px; border-radius: 20px; margin-bottom: 16px;">
                Reserva confirmada · Turno #{turno_id}
              </div>

              <h1 style="margin: 0 0 12px 0; color: #294d5d; font-size: 24px; font-weight: 800; line-height: 1.25;">
                ¡Tu turno ha sido reservado!
              </h1>

              <p style="margin: 0 0 24px 0; color: #5a687c; font-size: 15px; line-height: 1.5;">
                Hola <strong>{paciente_completo}</strong>, registramos tu reserva médica exitosamente. A continuación te presentamos el resumen de tu cita:
              </p>

              <!-- Tarjeta de detalle de reserva -->
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f7f9fa; border: 1px solid #e3e8ec; border-radius: 12px; margin-bottom: 24px;">
                <tr>
                  <td style="padding: 20px;">

                    <!-- Fecha y Hora destacadas -->
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border-bottom: 1px solid #e3e8ec; padding-bottom: 16px; margin-bottom: 16px;">
                      <tr>
                        <td style="vertical-align: middle;">
                          <div style="font-size: 12px; color: #788493; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Fecha y Horario</div>
                          <div style="font-size: 19px; font-weight: 800; color: #294d5d; margin-top: 2px;">{fecha_texto}</div>
                          <div style="font-size: 16px; font-weight: 700; color: #477f9a; margin-top: 2px;">{hora_texto}</div>
                        </td>
                      </tr>
                    </table>

                    <!-- Especialidad y Médico -->
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border-bottom: 1px solid #e3e8ec; padding-bottom: 16px; margin-bottom: 16px;">
                      <tr>
                        <td style="vertical-align: middle;">
                          <div style="font-size: 12px; color: #788493; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Profesional y Especialidad</div>
                          <div style="font-size: 16px; font-weight: 700; color: #354052; margin-top: 2px;">{medico_completo}</div>
                          <div style="display: inline-block; background-color: #ffffff; color: #4ca7a1; border: 1px solid #4ca7a1; font-size: 12px; font-weight: 600; padding: 2px 8px; border-radius: 6px; margin-top: 4px;">{especialidad}</div>
                        </td>
                      </tr>
                    </table>

                    <!-- Ubicación del consultorio -->
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                      <tr>
                        <td style="vertical-align: middle;">
                          <div style="font-size: 12px; color: #788493; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Ubicación en sede</div>
                          <div style="font-size: 15px; font-weight: 600; color: #354052; margin-top: 2px;">{consultorio_texto}</div>
                        </td>
                      </tr>
                    </table>

                  </td>
                </tr>
              </table>

              <!-- Recordatorio informativo -->
              <div style="background-color: #eaf3f7; border-left: 4px solid #477f9a; padding: 12px 16px; border-radius: 4px; margin-bottom: 28px;">
                <p style="margin: 0; font-size: 13px; color: #294d5d; line-height: 1.45;">
                  <strong>Importante:</strong> Te sugerimos presentarte 10 minutos antes del horario previsto con tu credencial y documento de identidad.
                </p>
              </div>

              <!-- Bloque de Acciones -->
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-bottom: 12px;">
                <tr>
                  <td align="center">
                    <!-- Botón de Cancelar Reserva -->
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin-bottom: 12px; width: 100%;">
                      <tr>
                        <td align="center" style="border-radius: 8px; background-color: #dc3545;">
                          <a href="{url_cancelar}" target="_blank" style="display: block; width: 100%; box-sizing: border-box; padding: 14px 24px; font-size: 15px; font-weight: 700; color: #ffffff; text-decoration: none; border-radius: 8px; text-align: center;">
                            Cancelar reserva
                          </a>
                        </td>
                      </tr>
                    </table>

                    <!-- Enlace secundario al portal -->
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="width: 100%;">
                      <tr>
                        <td align="center" style="border-radius: 8px; background-color: #f7f9fa; border: 1px solid #e3e8ec;">
                          <a href="{url_portal}" target="_blank" style="display: block; width: 100%; box-sizing: border-box; padding: 12px 24px; font-size: 14px; font-weight: 600; color: #477f9a; text-decoration: none; border-radius: 8px; text-align: center;">
                            Ver mis turnos en la web
                          </a>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>

              <p style="margin: 20px 0 0 0; font-size: 12px; color: #788493; text-align: center; line-height: 1.4;">
                Si sabés que no vas a poder concurrir, por favor cancelá tu reserva con tiempo mediante el botón rojo para liberar el horario para otro paciente.
              </p>

            </td>
          </tr>

          <!-- Pie de página -->
          <tr>
            <td style="background-color: #f7f9fa; border-top: 1px solid #e3e8ec; padding: 24px 32px; text-align: center;">
              <p style="margin: 0 0 6px 0; font-size: 13px; font-weight: 700; color: #294d5d;">Salud Integral · Centro Médico</p>
              <p style="margin: 0; font-size: 11px; color: #788493; line-height: 1.4;">
                Este es un mensaje automático de confirmación de reserva. Por favor no respondas a este correo.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    return cuerpo_html, cuerpo_texto


def enviar_correo(
    destinatario: str,
    asunto: str,
    cuerpo_html: str,
    cuerpo_texto: str | None = None
) -> bool:
    if not destinatario or not destinatario.strip():
        logging.warning("No se proporcionó un destinatario válido para enviar el correo.")
        return False

    smtp_host = os.getenv("SMTP_HOST", "localhost")
    smtp_port = int(os.getenv("SMTP_PORT", "1025"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    smtp_tls = os.getenv("SMTP_TLS", "False").lower() in ("true", "1")
    smtp_ssl = os.getenv("SMTP_SSL", "False").lower() in ("true", "1")
    remitente = os.getenv("EMAIL_REMITENTE", "Salud Integral <no-reply@saludintegral.com>")

    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = asunto
    mensaje["From"] = remitente
    mensaje["To"] = destinatario.strip()

    if cuerpo_texto:
        mensaje.attach(MIMEText(cuerpo_texto, "plain", "utf-8"))
    mensaje.attach(MIMEText(cuerpo_html, "html", "utf-8"))

    try:
        if smtp_ssl:
            servidor = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=5)
        else:
            servidor = smtplib.SMTP(smtp_host, smtp_port, timeout=5)

        with servidor:
            if smtp_tls and not smtp_ssl:
                servidor.starttls()
            if smtp_user and smtp_password:
                servidor.login(smtp_user, smtp_password)
            servidor.send_message(mensaje)

        logging.info("Aviso de correo enviado exitosamente a %s", destinatario)
        return True
    except Exception as error:
        logging.warning("No fue posible despachar el correo a %s: %s", destinatario, error)
        return False


def enviar_aviso_reserva(turno_id: int) -> bool:
    connection = get_db_connection()
    try:
        datos_turno = turno_repo.obtener_turno_con_detalles_para_correo(connection, turno_id)
        if not datos_turno:
            logging.warning("No se encontraron detalles para el turno #%s al enviar aviso.", turno_id)
            return False

        destinatario = datos_turno.get("paciente_email")
        if not destinatario:
            logging.warning("El paciente del turno #%s no posee correo registrado.", turno_id)
            return False

        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5001").rstrip("/")
        token = datos_turno.get("qr_token") or ""

        url_cancelar = f"{frontend_url}/cancelar-reserva?turno_id={turno_id}&token={token}"
        url_portal = f"{frontend_url}/mis-turnos/{turno_id}"

        cuerpo_html, cuerpo_texto = generar_plantilla_reserva(
            datos_turno=datos_turno,
            url_cancelar=url_cancelar,
            url_portal=url_portal
        )

        asunto = f"Confirmación de tu reserva · Turno #{turno_id} - Salud Integral"
        return enviar_correo(
            destinatario=destinatario,
            asunto=asunto,
            cuerpo_html=cuerpo_html,
            cuerpo_texto=cuerpo_texto
        )
    finally:
        connection.close()

