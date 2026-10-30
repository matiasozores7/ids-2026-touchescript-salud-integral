from flask import jsonify

def success_response(data=None, message="Operación realizada correctamente.", status_code=200):
    response = {
        "status": "ok",
        "message": message
    }

    if data is not None:
        response["data"] = data

    return jsonify(response), status_code