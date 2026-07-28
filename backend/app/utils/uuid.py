import uuid
from typing import Optional

def generate_uuid() -> uuid.UUID:
    """Generate a standard cryptographically secure random UUIDv4."""
    return uuid.uuid4()

def is_valid_uuid(val: str) -> bool:
    """Check if the provided string is a valid UUID representation."""
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

def parse_uuid(val: str) -> Optional[uuid.UUID]:
    """Parse a string representation of a UUID, returns None if invalid."""
    try:
        return uuid.UUID(str(val))
    except ValueError:
        return None
