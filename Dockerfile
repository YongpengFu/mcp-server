# Use the official uv Python image with Python 3.12
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set working directory
WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Copy the application code (including resource directory)
COPY . .

# Ensure resource directory exists and has proper permissions
RUN mkdir -p /app/resource && chmod 755 /app/resource

# Expose the port that FastMCP typically uses (you may need to adjust this)
EXPOSE 8000

# Run the application using uv
CMD ["uv", "run", "server.py"] 