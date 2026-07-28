import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict
from app.utils.time import get_utc_now

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        # Standard schema context keys
        log_payload: Dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "func_name": record.funcName,
            "line_no": record.lineno,
        }
        
        # Inject correlation id if present on the log record (added via middleware)
        correlation_id = getattr(record, "correlation_id", None)
        if correlation_id:
            log_payload["correlation_id"] = correlation_id

        # Inject exception details if present
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)

        # Inject extra fields if present
        if hasattr(record, "extra_fields"):
            log_payload.update(record.extra_fields)  # type: ignore

        return json.dumps(log_payload)

def setup_logging() -> None:
    root_logger = logging.getLogger()
    
    # Avoid duplicate handlers if setup is called multiple times
    if root_logger.handlers:
        return

    root_logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(console_handler)

    # Patch third party uvicorn loggers to use the same handler
    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        log = logging.getLogger(logger_name)
        log.handlers = []
        log.propagate = True
