from enum import Enum

class UserStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    PENDING = "pending"

class IncidentStatus(str, Enum):
    TRIGGERED = "triggered"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"

class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class HealthState(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"
    UNKNOWN = "unknown"

class AIProviderType(str, Enum):
    OFFLINE = "offline"
    FREE_ONLINE = "free_online"
    PAID = "paid"

class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    SKIPPED = "skipped"

class ThemePreference(str, Enum):
    AZURE_COMMAND = "azure-command"
    CYBERPUNK_NEON = "cyberpunk-neon"
    MATRIX_TERMINAL = "matrix-terminal"
    ENTERPRISE_DARK = "enterprise-dark"
    ARCTIC_ICE = "arctic-ice"
    SUNSET_ORANGE = "sunset-orange"
    MIDNIGHT_PURPLE = "midnight-purple"

class PermissionScope(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
