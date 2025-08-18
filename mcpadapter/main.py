import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print(f"OPENAI_API_KEY: {api_key}")


async def main():
    print("Hello from mcpadapter!")

if __name__ == "__main__":
    asyncio.run(main())
