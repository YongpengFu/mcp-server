# Terminal MCP Server

A simple MCP (Model Context Protocol) server that exposes a terminal tool and a resource for running shell commands and accessing documentation.

## Features

- **Terminal Tool**: Execute shell commands and get their output
- **Resource Support**: Access the MCP readme documentation file
- **Working Directory Support**: Optionally specify a working directory for commands
- **Timeout Protection**: Commands timeout after 30 seconds
- **Error Handling**: Proper error handling for failed commands

## Installation

The project uses `uv` for dependency management. Install dependencies:

```bash
uv sync
```

## Usage

### Running the Server

```bash
python server.py
```

### Tools

The server exposes a single tool called `terminal` with the following schema:

```json
{
  "name": "terminal",
  "description": "Run terminal commands and return the output",
  "inputSchema": {
    "type": "object",
    "properties": {
      "command": {
        "type": "string",
        "description": "The shell command to execute"
      },
      "cwd": {
        "type": "string",
        "description": "Working directory for the command (optional)"
      }
    },
    "required": ["command"]
  }
}
```

### Example Usage

The tool can be called with:

```json
{
  "command": "ls -la",
  "cwd": "/path/to/directory"
}
```

### Resources

The server exposes a resource for accessing the MCP readme documentation:

- **URI**: `file:///Users/yongpengfu/Desktop/Desktop/Desktop/Language/Data_Engineering/MCP/mcp-servers/quickstart-resources/resource/mcpreadme.md`
- **Name**: MCP Readme
- **Description**: MCP documentation and readme file
- **MIME Type**: `text/markdown`

This resource allows clients to read the MCP documentation directly through the server.

## Security Note

⚠️ **Warning**: This server allows execution of arbitrary shell commands. Use with caution and only in trusted environments.

## Dependencies

- `mcp[cli]>=1.13.0` - MCP Python SDK
