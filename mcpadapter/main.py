import asyncio
import os

from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables from .env file
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
stdio_server_parameters = StdioServerParameters(
    command="uv",
    args=["run", "servers/math_server.py"],
    env=os.environ,
    cwd=os.path.dirname(os.path.abspath(__file__)),
    log_level="INFO",
)


async def main():
    print("Hello from mcpadapter!")


if __name__ == "__main__":
    asyncio.run(main())
