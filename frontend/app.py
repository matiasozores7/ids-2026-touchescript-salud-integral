from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("login.html")

@app.get("/mis-turnos")
def mis_turnos():
    return render_template("pacientes/mis_turnos.html")

@app.get("/mis-turnos/<int:turno_id>")
def detalle_turno(turno_id):
    return render_template("pacientes/detalle_turno.html", turno_id=turno_id)

@app.get("/qr/<int:turno_id>")
def qr_turno(turno_id):
    return render_template("pacientes/qr_turno.html", turno_id=turno_id)

@app.get("/backoffice/consultorios")
def backoffice_consultorios():
    return render_template("backoffice/consultorios.html")

@app.route("/backoffice/consultorios/nuevo", methods=["GET", "POST"])
@app.route("/backoffice/consultorios/<int:consultorio_id>/editar", methods=["GET", "POST"])
def backoffice_consultorio_form(consultorio_id=None):
    return render_template("backoffice/consultorio_form.html")

@app.get("/backoffice/check-in")
def backoffice_checkin():
    return render_template("recepcion/checkin.html")

@app.post("/login")
def login():
    role = request.form.get("role", "paciente")
    destination = "backoffice" if role in {"recepcion", "administracion"} else "patient_home"
    return redirect(url_for(destination))

@app.route("/pacientes", methods=["GET", "POST"])
def patient_home():
    return render_template("pacientes/home.html")

@app.route("/registro")
def patient_register():
    return render_template("pacientes/register.html")

@app.route("/backoffice")
def backoffice():
    return render_template("backoffice/backoffice.html")

@app.route("/backoffice/especialidades", methods=["GET", "POST"])
def backoffice_specialties():
    return render_template("backoffice/specialties.html")

if __name__ == "__main__":
    app.run(port=5001, debug=True)

