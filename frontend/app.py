from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("login.html")

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
