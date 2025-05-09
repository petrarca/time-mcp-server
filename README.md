# Time MCP Server

A Model Context Protocol server for time-related functionality.

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

Run the application:
```
task run
```

## Development

- Format code: `task format`
- Check and fix linting issues: `task check`
- Run tests: `task test`
