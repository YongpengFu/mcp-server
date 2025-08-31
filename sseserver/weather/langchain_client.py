from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import asyncio

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


async def main():
    print("Starting weather MCP client...")

    # Create the client with server configurations
    client = MultiServerMCPClient({
        "math": {
            "command": "uv",
            "args": ["run", "math.py"],
            "transport": "stdio"  # Added missing transport key
        },
        "weather": {
            "url": "http://localhost:8000/sse",
            "transport": "sse"
        },
    })

    # Get the tools from all servers
    tools = await client.get_tools()

    # Create the agent with the tools
    agent = create_react_agent(llm, tools)

    # Test weather query
    result = await agent.ainvoke({
        "messages": [HumanMessage(content="What is the weather in Tokyo?")]
    })
    print(result["messages"][-1].content)

    # Test math query
    result = await agent.ainvoke({
        "messages": [HumanMessage(content="What is 1 + 3* 12 + 10?")]
    })
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
