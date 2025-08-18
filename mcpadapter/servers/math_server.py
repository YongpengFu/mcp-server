from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="math_server")


@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b


@mcp.tool()
def subtract(a: int, b: int) -> int:
    return a - b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == "__main__":
    mcp.run()
