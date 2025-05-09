"""Tests for the Time MCP Server using a FastMCP client."""

import asyncio
import datetime
import json

import pytest
from fastmcp import Client

from time_mcp_server.server import mcp


@pytest.mark.asyncio
async def test_get_current_time() -> None:
    """Test the get_current_time tool using an in-memory client."""
    # Connect to the server using the in-memory transport
    async with Client(mcp) as client:
        # List available tools
        tools = await client.list_tools()
        tool_names = [tool.name for tool in tools]

        # Verify our tools are available
        assert "get_current_time" in tool_names
        assert "get_time_components" in tool_names

        # Call the get_current_time tool without a format
        result = await client.call_tool("get_current_time")
        # FastMCP client returns a list with a single item for the result
        text_content = result[0]

        # Parse the JSON string from the text content
        time_data = json.loads(text_content.text)

        # Verify the response structure
        assert isinstance(time_data, dict)
        assert "iso_time" in time_data
        assert "formatted_time" in time_data
        assert "timezone" in time_data

        # Verify the times are the same (since no format was provided)
        assert time_data["iso_time"] == time_data["formatted_time"]

        # Verify the default timezone is Berlin
        assert "Europe/Berlin" in time_data["timezone"]

        # Call the get_current_time tool with a custom format
        custom_format = "%Y-%m-%d %H:%M:%S"
        result = await client.call_tool("get_current_time", {"date_format": custom_format})
        # FastMCP client returns a list with a single item for the result
        text_content = result[0]

        # Parse the JSON string from the text content
        time_data = json.loads(text_content.text)

        # Verify the formatted time matches the expected format
        # We can't check the exact time, but we can verify the format is correct
        assert len(time_data["formatted_time"]) == len(datetime.datetime.now().strftime(custom_format))

        # Test with a custom timezone
        custom_timezone = "America/New_York"
        result = await client.call_tool("get_current_time", {"timezone": custom_timezone})
        text_content = result[0]
        time_data = json.loads(text_content.text)

        # Verify the timezone is correctly set
        assert custom_timezone in time_data["timezone"]


@pytest.mark.asyncio
async def test_get_time_components() -> None:
    """Test the get_time_components tool using an in-memory client."""
    # Connect to the server using the in-memory transport
    async with Client(mcp) as client:
        # Call the get_time_components tool
        result = await client.call_tool("get_time_components")
        # FastMCP client returns a list with a single item for the result
        text_content = result[0]

        # Parse the JSON string from the text content
        components = json.loads(text_content.text)

        # Verify the response structure
        assert isinstance(components, dict)

        # Check all expected keys are present
        expected_keys = ["year", "month", "day", "hour", "minute", "second", "microsecond", "weekday", "timezone"]
        for key in expected_keys:
            assert key in components

        # Verify the default timezone is Berlin
        assert "Europe/Berlin" in components["timezone"]

        # Verify the types of the components
        assert isinstance(components["year"], int)
        assert isinstance(components["month"], int)
        assert isinstance(components["day"], int)
        assert isinstance(components["hour"], int)
        assert isinstance(components["minute"], int)
        assert isinstance(components["second"], int)
        assert isinstance(components["microsecond"], int)
        assert isinstance(components["weekday"], int)

        # Verify the values are within expected ranges
        assert 2000 <= components["year"] <= 2100  # Reasonable year range
        assert 1 <= components["month"] <= 12
        assert 1 <= components["day"] <= 31
        assert 0 <= components["hour"] <= 23
        assert 0 <= components["minute"] <= 59
        assert 0 <= components["second"] <= 59
        assert 0 <= components["microsecond"] <= 999999
        assert 0 <= components["weekday"] <= 6  # 0 is Monday, 6 is Sunday

        # Test with a custom timezone
        custom_timezone = "America/New_York"
        result = await client.call_tool("get_time_components", {"timezone": custom_timezone})
        text_content = result[0]
        components = json.loads(text_content.text)

        # Verify the timezone is correctly set
        assert custom_timezone in components["timezone"]

        # Verify the time components are within expected ranges
        assert 2000 <= components["year"] <= 2100
        assert 1 <= components["month"] <= 12
        assert 1 <= components["day"] <= 31
        assert 0 <= components["hour"] <= 23
        assert 0 <= components["minute"] <= 59
        assert 0 <= components["second"] <= 59


if __name__ == "__main__":
    # Run the tests directly
    asyncio.run(test_get_current_time())
    asyncio.run(test_get_time_components())
    print("All tests passed!")
