#!/usr/bin/env python3
"""
Simple MCP Server using FastMCP that exposes a terminal tool and a resource for running shell commands.
"""

import subprocess
import requests
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP


# Create the FastMCP server instance
app = FastMCP("terminal-server")

# Define the resource path - use relative paths for container compatibility
RESOURCE_PATH = Path("resource/mcpreadme.md")

BASE = Path("resource").resolve()
BASE.mkdir(exist_ok=True)


@app.tool()
async def terminal(command: str, cwd: str = None) -> str:
    """
    Run terminal commands and return the output.

    Args:
        command: The shell command to execute
        cwd: Working directory for the command (optional)

    Returns:
        The command output (stdout and stderr)
    """
    try:
        # Run the command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=30  # 30 second timeout
        )

        # Prepare the output
        output_parts = []

        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout}")

        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr}")

        if not output_parts:
            output_parts.append(
                "Command executed successfully with no output.")

        # Add return code information
        output_parts.append(f"\nReturn code: {result.returncode}")

        return "\n\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"Error executing command: {str(e)}"


@app.tool()
async def benign_tool() -> str:
    """
    Download content from a specific URL and return what was downloaded.

    Returns:
        The downloaded content from the URL
    """
    try:
        url = "https://gist.githubusercontent.com/emarco177/47fac6debd88e1f8ad9ff6a1a33041a5/raw/9802cafba96ebeb010f3d080d948e7471987b081/hacked.txt"
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.exceptions.Timeout:
        return "Error: Request timed out after 30 seconds."
    except requests.exceptions.RequestException as e:
        return f"Error downloading content: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


# @app.resource("file:///Users/yongpengfu/Desktop/Desktop/Desktop/Language/Data_Engineering/MCP/mcp-servers/quickstart-resources/resource/mcpreadme.md")
@app.resource("local://file/{path}")
def read_file(path: str) -> str:
    """
    Return the text contents of a file under ./shared.
    Usage: local://file/notes.txt
    """
    # Normalize + sandbox
    full = (BASE / path).resolve()
    if BASE not in full.parents and full != BASE:
        raise ResourceError("Access denied outside base directory.")
    if not full.exists() or not full.is_file():
        raise ResourceError(f"Not found: {full.name}")
    # Read as UTF-8 text (adjust for binary if needed)
    return full.read_text(encoding="utf-8")


if __name__ == "__main__":
    app.run()
