from flask import Flask, render_template

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("login.html")


@app.post("/pacientes")
def patient_home():
    return render_template("pacientes/inicio.html")


if __name__ == "__main__":
    app.run(port=5001, debug=True)
