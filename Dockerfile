FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv installer
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh

# Copy project files
COPY pyproject.toml uv.lock ./
COPY app ./app
COPY data ./data

# Setup virtualenv via uv and install dependencies
RUN uv sync --frozen

# Start streamlit
EXPOSE 8501

CMD ["uv", "run", "python", "-m", "streamlit", "run", "app/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
