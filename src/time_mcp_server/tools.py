"""Time tools implementation for the Time MCP Server."""

from datetime import datetime
import zoneinfo
from typing import Dict, Optional


def get_current_time(date_format: Optional[str] = None, timezone: str = "Europe/Berlin") -> Dict[str, str]:
    """
    Get the current date and time.

    Args:
        date_format: Optional format string for the datetime (e.g., '%Y-%m-%d %H:%M:%S').
                    If not provided, ISO format will be used.
        timezone: Timezone name (e.g., 'Europe/Berlin', 'America/New_York').
                 If not provided, 'Europe/Berlin' will be used as default.

    Returns:
        A dictionary containing the current time in the requested format, ISO format, and the timezone used.
    """
    tz = zoneinfo.ZoneInfo(timezone)
    now = datetime.now(tz)

    # Default ISO format
    iso_time = now.isoformat()

    # Custom format if provided
    formatted_time = now.strftime(date_format) if date_format else iso_time

    return {
        "iso_time": iso_time,
        "formatted_time": formatted_time,
        "timezone": timezone,
    }


def get_time_components(timezone: str = "Europe/Berlin") -> Dict[str, int]:
    """
    Get the components of the current time.

    Args:
        timezone: Timezone name (e.g., 'Europe/Berlin', 'America/New_York').
                 If not provided, 'Europe/Berlin' will be used as default.

    Returns:
        A dictionary containing the year, month, day, hour, minute, second, microsecond, weekday, and timezone.
    """
    tz = zoneinfo.ZoneInfo(timezone)
    now = datetime.now(tz)

    return {
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "hour": now.hour,
        "minute": now.minute,
        "second": now.second,
        "microsecond": now.microsecond,
        "weekday": now.weekday(),  # 0 is Monday, 6 is Sunday
        "timezone": timezone,
    }
