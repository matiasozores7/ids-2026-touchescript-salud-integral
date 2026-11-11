from app.clients.api_client import api_request


def realizar_checkin(qr_token: str) -> None:
    api_request(
        method="POST",
        endpoint="/turnos/checkin",
        json={"qr_token": qr_token},
        authenticated=True,
    )