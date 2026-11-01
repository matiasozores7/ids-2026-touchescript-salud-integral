from flask import Flask, render_template

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("pacientes/inicio.html")

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

if __name__ == "__main__":
    app.run(port=5001, debug=True)
