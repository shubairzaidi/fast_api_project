from typing import Optional, Union
from fastapi.responses import JSONResponse # type: ignore
from datetime import datetime, date
from sqlalchemy.orm import DeclarativeMeta # type: ignore

def custom_http_response(
    status_code: int,
    success: bool,
    message: str,
    data: Optional[Union[dict, list]] = None,
    total_count: int = 0,
    total_pages: int = 0,
    page: int = 0,
    size: int = 0
):
    def serialize(obj):
        """Recursively convert SQLAlchemy objects to dict and handle datetime."""
        if isinstance(obj, list):
            return [serialize(item) for item in obj]
        elif hasattr(obj, "__table__"):  # SQLAlchemy model
            result = {}
            for c in obj.__table__.columns:
                value = getattr(obj, c.name)
                if isinstance(value, (datetime, date)):
                    result[c.name] = value.isoformat()
                else:
                    result[c.name] = value
            return result
        elif isinstance(obj, dict):
            return {k: serialize(v) for k, v in obj.items()}
        else:
            return obj

    serialized_data = serialize(data) if data else {}

    return JSONResponse(
        status_code=status_code,
        content={
            "success": success,
            "message": message,
            "data": serialized_data,
            "total_count": total_count,
            "total_pages": total_pages,
            "page": page,
            "size": size
        }
    )
