import time
import uuid
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("http")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id") or uuid.uuid4().hex
        start = time.perf_counter()

        response = await call_next(request)

        ms = (time.perf_counter() - start) * 1000
        logger.info(
            "request",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_ms": round(ms, 2),
                "client": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
            },
        )

        response.headers["x-request-id"] = request_id
        return response