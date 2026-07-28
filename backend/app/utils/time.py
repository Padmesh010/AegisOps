from datetime import datetime, timezone

def get_utc_now() -> datetime:
    """Return the current time in UTC with explicit timezone info."""
    return datetime.now(timezone.utc)

def format_timestamp(dt: datetime) -> str:
    """Format datetime as ISO 8601 string in UTC."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()
