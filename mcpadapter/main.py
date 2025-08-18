import asyncio
import os

from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
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
    print("Starting MCP adapter...")

    # Connect to the MCP server using stdio
    async with stdio_client(stdio_server_parameters) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            # tools = await session.list_tools()
            print(tools)
            agent = create_react_agent(llm, tools)
            result = await agent.ainvoke({"messages": [HumanMessage(content="What is the capital of France?")]})
            print(result["messages"][-1].content)
            result = await agent.ainvoke({"messages": [HumanMessage(content="What is 1 + 3* 12 + 10?")]})
            print(result["messages"][-1].content)

        print("Connected to MCP server successfully!")

        print("MCP adapter completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
