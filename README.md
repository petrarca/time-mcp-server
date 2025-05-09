# Time MCP Server

A Model Context Protocol (MCP) server that provides time-related tools for Large Language Models. Built with FastMCP 2.0.

## Setup

This project uses `uv` for Python package management and `task` for running common commands.

### Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver
- [Task](https://taskfile.dev/) - Task runner / build tool

### Installation

1. Clone the repository
2. Run the setup task to create a virtual environment:
   ```
   task setup
   ```
3. Install the package in development mode:
   ```
   task install
   ```

## Usage

### Running the Server

Run the MCP server using the task runner:
```
task run
```

By default, the server will start using the `stdio` transport, which is ideal for connecting with Claude Desktop and other local MCP clients.

#### Command-line Options

You can configure the transport type and port:

```
# Run with stdio transport (default)
python -m time_mcp_server.main --transport stdio

# Run with HTTP transport on port 9000
python -m time_mcp_server.main --transport streamable-http --port 9000
```

Or when using the task runner, you can pass arguments after `--`:

```
# Run with stdio transport (default)
task run

# Run with HTTP transport
task run -- --transport streamable-http --port 9000
```

### Available Tools

The Time MCP Server provides the following tools for LLMs:

1. **get_current_time** - Get the current date and time
   - Parameters:
     - `date_format` (optional): Format string for the datetime (e.g., '%Y-%m-%d %H:%M:%S')
   - Returns: A dictionary with the current time in ISO format and the requested format

2. **get_time_components** - Get the components of the current time
   - Returns: A dictionary with year, month, day, hour, minute, second, microsecond, and weekday

### Example Client Usage

To use this MCP server with an LLM client, connect to the server endpoint and call the tools:

```python
import asyncio
from fastmcp import Client

async def main():
    # Connect to the Time MCP Server
    # Make sure to include the /mcp path in the URL
    async with Client("http://localhost:8090/mcp") as client:
        # Get the current time
        result = await client.call_tool("get_current_time", {"date_format": "%Y-%m-%d %H:%M:%S"})
        # Parse the JSON response
        import json
        time_data = json.loads(result[0].text)
        print(time_data)
        # Output: {'iso_time': '2025-05-09T16:27:31.123456', 'formatted_time': '2025-05-09 16:27:31'}
        
        # Get time components
        result = await client.call_tool("get_time_components")
        components = json.loads(result[0].text)
        print(components)
        # Output: {'year': 2025, 'month': 5, 'day': 9, 'hour': 16, 'minute': 27, 'second': 31, 'microsecond': 123456, 'weekday': 4}

# Run the async client
asyncio.run(main())
```

## Connecting to Claude Desktop

The Time MCP Server can be easily connected to Claude Desktop since it now uses stdio transport by default. Here's how to set it up:

1. Open Claude Desktop
2. Click on the "Claude" menu in the top bar (on macOS) or the appropriate menu on Windows
3. Select "Settings..." and then navigate to "Developer" > "Edit Config"
4. Add your Time MCP Server to the configuration file:

```json
{
  "mcpServers": {
    "current-time": {
      "command": "/path/to/uv",
      "args": [
        "run", "--directory", "/path/to/time-mcp-server", "python", "-m", "time_mcp_server.main"
      ]
    }
  }
}
```

Make sure to replace `/path/to/uv` with the path to your uv executable and `/path/to/time-mcp-server` with the actual path to your project directory.

5. Save the configuration file and restart Claude Desktop
6. You should see a hammer icon in the bottom right corner of Claude's input box
7. Clicking on it will show your Time MCP Server's tools

Now you can ask Claude to use your time tools, such as:
- "What's the current time?"
- "Can you tell me the current date in YYYY-MM-DD format?"
- "What day of the week is it today?"

## Development

- Format code: `task format`
- Check and fix linting issues: `task check`
- Run tests: `task test`

### Testing

The project includes tests that demonstrate how to use the Time MCP Server as a client. The tests use FastMCP's in-memory client to connect directly to the server without requiring a network connection.

```python
# Example of using the FastMCP client to connect to the server
from fastmcp import Client
from time_mcp_server.server import mcp

async with Client(mcp) as client:
    # List available tools
    tools = await client.list_tools()
    
    # Call the get_current_time tool
    result = await client.call_tool("get_current_time", {"date_format": "%Y-%m-%d %H:%M:%S"})
    text_content = result[0]
    
    # Parse the JSON response
    import json
    time_data = json.loads(text_content.text)
    print(time_data)
```

Run the tests with:

```
task test
```
