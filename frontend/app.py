from flask import Flask, render_template

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("pacientes/inicio.html")

@app.get("/mis-turnos")
def mis_turnos():
    return render_template("pacientes/mis_turnos.html")

@app.get("/mis-turnos/<int:turno_id>")
def detalle_turno(turno_id):
    return render_template("pacientes/detalle_turno.html", turno_id=turno_id)

@app.get("/qr/<int:turno_id>")
def qr_turno(turno_id):
    return render_template("pacientes/qr_turno.html", turno_id=turno_id)

if __name__ == "__main__":
    app.run(port=5001, debug=True)

