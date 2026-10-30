from flask import Flask, render_template

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("login.html")


@app.post("/pacientes")
def patient_home():
    return render_template("pacientes/inicio.html")

@app.route("/registro")
def patient_register():
    return render_template("pacientes/register.html")


if __name__ == "__main__":
    app.run(port=5001, debug=True)
