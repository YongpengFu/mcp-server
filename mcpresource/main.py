from fastmcp import FastMCP

mcp = FastMCP("mcpresource")


@mcp.prompt("get_research_prompt")
def get_research_prompt(query: str) -> str:
    """Get a research prompt for a given query."""
    return f"Hello, world! {query}"


if __name__ == "__main__":
    mcp.run(transport="http")
