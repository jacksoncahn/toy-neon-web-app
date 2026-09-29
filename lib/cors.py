CORS_ORIGIN = "http://localhost:3000"

CORS_HEADERS = {
    "Access-Control-Allow-Origin": CORS_ORIGIN,
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, user_id, Authorization",
    "Access-Control-Allow-Private-Network": "true",
    "Vary": "Origin",
}


def allowed_origins() -> list[str]:
    return [CORS_ORIGIN]
