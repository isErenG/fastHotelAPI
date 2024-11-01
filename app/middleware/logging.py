import time

from fastapi.logger import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse


class LoggingMiddleware(BaseHTTPMiddleware):
    SLOW_REQUEST_THRESHOLD = 1.0

    async def dispatch(self, request: Request, call_next):
        logger.debug(f"Incoming request: {request.method} {request.url}")

        start_time = time.time()

        try:
            response = await call_next(request)
        except Exception as e:
            logger.warning(f"Request failed: {request.method} {request.url} - Error: {str(e)}")

            return PlainTextResponse("Internal server error", status_code=500)

        process_time = time.time() - start_time

        logger.debug(
            f"Response: status code {response.status_code} processed in {process_time:.4f} seconds"
        )

        if response.status_code < 400:
            logger.info(f"Request completed: {request.method} {request.url} - Status: {response.status_code}")

        if process_time > self.SLOW_REQUEST_THRESHOLD:
            logger.warning(
                f"Slow request: {request.method} {request.url} took {process_time:.4f} seconds to process"
            )

        return response
