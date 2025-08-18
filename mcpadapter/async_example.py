import asyncio
import time


# ============================================================================
# EXAMPLE 1: Basic async/await - Simulating slow operations
# ============================================================================

async def fetch_user_data(user_id):
    """Simulate fetching user data from a database"""
    print(f"🔄 Starting to fetch data for user {user_id}")
    await asyncio.sleep(2)  # Simulate database delay
    print(f"✅ Finished fetching data for user {user_id}")
    return f"User data for {user_id}"


async def send_email(user_id):
    """Simulate sending an email"""
    print(f"📧 Starting to send email to user {user_id}")
    await asyncio.sleep(1)  # Simulate email delay
    print(f"✅ Email sent to user {user_id}")
    return f"Email sent to {user_id}"


# ============================================================================
# EXAMPLE 2: Sequential vs Concurrent execution
# ============================================================================

async def sequential_example():
    """Run operations one after another (slow)"""
    print("\n🐌 SEQUENTIAL EXECUTION (Slow):")
    start_time = time.time()

    # These run one after another
    user_data = await fetch_user_data(1)  # 2 seconds
    email_result = await send_email(1)     # 1 second

    total_time = time.time() - start_time
    print(f"⏱️  Total time: {total_time:.1f} seconds")
    print(f"📊 Results: {user_data}, {email_result}")


async def concurent_example():
    """Run operations at the same time (fast)"""
    print("\n⚡ CONCURRENT EXECUTION (Fast):")
    start_time = time.time()

    # These run at the same time
    user_data, email_result = await asyncio.gather(
        fetch_user_data(2),  # 2 seconds
        send_email(2)        # 1 second (runs simultaneously)
    )

    total_time = time.time() - start_time
    print(f"⏱️  Total time: {total_time:.1f} seconds")
    print(f"📊 Results: {user_data}, {email_result}")


# ============================================================================
# EXAMPLE 3: Real-world scenario - Multiple API calls
# ============================================================================

async def fetch_weather(city):
    """Simulate fetching weather data"""
    print(f"🌤️  Fetching weather for {city}")
    await asyncio.sleep(1)
    return f"Weather in {city}: Sunny, 25°C"


async def fetch_news(category):
    """Simulate fetching news data"""
    print(f"📰 Fetching {category} news")
    await asyncio.sleep(1.5)
    return f"Latest {category} news: AI breakthrough!"


async def fetch_stock_price(symbol):
    """Simulate fetching stock data"""
    print(f"📈 Fetching stock price for {symbol}")
    await asyncio.sleep(0.5)
    return f"{symbol} stock: $150.00"


async def dashboard_example():
    """Simulate a dashboard that needs data from multiple sources"""
    print("\n📊 DASHBOARD EXAMPLE - Multiple API Calls:")
    start_time = time.time()

    # Fetch all data concurrently
    weather, news, stock = await asyncio.gather(
        fetch_weather("Toronto"),
        fetch_news("Technology"),
        fetch_stock_price("AAPL")
    )

    total_time = time.time() - start_time
    print(f"\n⏱️  Total time: {total_time:.1f} seconds")
    print(f"📊 Dashboard Data:")
    print(f"   {weather}")
    print(f"   {news}")
    print(f"   {stock}")


# ============================================================================
# EXAMPLE 4: Error handling with async
# ============================================================================

async def risky_operation():
    """Simulate an operation that might fail"""
    await asyncio.sleep(1)
    if time.time() % 2 < 1:  # 50% chance of failure
        raise Exception("Something went wrong!")
    return "Operation successful!"


async def error_handling_example():
    """Show how to handle errors in async code"""
    print("\n🛡️  ERROR HANDLING EXAMPLE:")

    try:
        result = await risky_operation()
        print(f"✅ {result}")
    except Exception as e:
        print(f"❌ Error caught: {e}")


# ============================================================================
# MAIN FUNCTION - Run all examples
# ============================================================================

async def main():
    """Run all the examples"""
    print("🚀 ASYNC/AWAIT EXAMPLES")
    print("=" * 50)

    # Run examples
    await sequential_example()
    await concurrent_example()
    # await dashboard_example()
    # await error_handling_example()

    print("\n🎉 All examples completed!")


# ============================================================================
# HOW TO RUN THIS CODE
# ============================================================================

if __name__ == "__main__":
    # This is how you run async code from the main script
    asyncio.run(main())
