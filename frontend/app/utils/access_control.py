from flask import abort, g, redirect, url_for, session

from app.services import auth_service
from app.errors.exceptions import AuthenticationError


def proteger_por_rol(*roles_permitidos):

    def verificar_acceso():
        if not session.get("access_token"):
            return redirect(url_for("auth.mostrar_login"))

        try:
            usuario = auth_service.obtener_usuario_actual()

        except AuthenticationError:
            session.clear()
            return redirect(url_for("auth.mostrar_login"))

        if usuario.get("rol") not in roles_permitidos:
            abort(403)

        g.usuario = usuario

    return verificar_acceso