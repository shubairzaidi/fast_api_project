from fastapi.responses import JSONResponse

def custom_http_response(status_code: int, success: bool, message: str, data: dict = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": success,
            "message": message,
            "data": data or {}
        }
    )
