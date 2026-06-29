"""Offensive operations (guardrailed, authorized testing only)."""

from WiFiHound.operations.base import (  # noqa: F401
    OperationError,
    OperationNotAuthorized,
    offensive_available,
)
from WiFiHound.operations import enterprise  # noqa: F401

__all__ = [
    "OperationError",
    "OperationNotAuthorized",
    "offensive_available",
    "enterprise",
]
