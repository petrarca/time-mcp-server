"""Time tools implementation for the Time MCP Server."""

from datetime import datetime
from typing import Dict, Optional

import pytz


def get_current_time(date_format: Optional[str] = None, timezone: Optional[str] = None) -> Dict[str, str]:
    """
    Get the current date and time.

    Args:
        date_format: Optional format string for the datetime (e.g., '%Y-%m-%d %H:%M:%S').
                    If not provided, ISO format will be used.
        timezone: Optional timezone name (e.g., 'Europe/Berlin', 'America/New_York').
                 If not provided, 'Europe/Berlin' will be used as default.

    Returns:
        A dictionary containing the current time in the requested format and ISO format,
        along with the timezone used.
    """
    # Use Berlin as default timezone if not specified
    tz = pytz.timezone(timezone if timezone else "Europe/Berlin")

    # Get current time in the specified timezone
    now = datetime.now(tz)

    # Default ISO format
    iso_time = now.isoformat()

    # Custom format if provided
    formatted_time = now.strftime(date_format) if date_format else iso_time

    return {"iso_time": iso_time, "formatted_time": formatted_time, "timezone": str(tz)}


def get_time_components(timezone: Optional[str] = None) -> Dict[str, int]:
    """
    Get the components of the current time.

    Args:
        timezone: Optional timezone name (e.g., 'Europe/Berlin', 'America/New_York').
                 If not provided, 'Europe/Berlin' will be used as default.

    Returns:
        A dictionary containing the year, month, day, hour, minute, second, microsecond,
        weekday, and timezone information.
    """
    # Use Berlin as default timezone if not specified
    tz = pytz.timezone(timezone if timezone else "Europe/Berlin")

    # Get current time in the specified timezone
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
        "timezone": str(tz),
    }
