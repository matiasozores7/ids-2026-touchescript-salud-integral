from flask import Flask

app = Flask(__name__)


@app.route('/api/healthcheck', methods=['GET'])
def healthcheck():
    return {
        "status": "ok",
        "message": "API Backend activa"
    }, 200


if __name__ == '__main__':
    app.run(port=5000, debug=True)