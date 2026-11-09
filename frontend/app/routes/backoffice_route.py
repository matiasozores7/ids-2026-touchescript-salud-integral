from flask import Blueprint, render_template

from app.constants.roles import ADMIN
from app.utils.access_control import proteger_por_rol

backoffice_bp = Blueprint("backoffice", __name__)

backoffice_bp.before_request(proteger_por_rol(ADMIN))


@backoffice_bp.route("/", methods=["GET"])
def dashboard():
    return render_template("backoffice/backoffice.html")