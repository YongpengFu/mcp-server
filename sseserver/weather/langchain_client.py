from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import asyncio
load_dotenv()

client = MultiServerMCPClient()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


async def main():
    print("Starting weather MCP client...")

if __name__ == "__main__":
    asyncio.run(main())
