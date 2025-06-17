FROM python:3.11-alpine AS builder

WORKDIR /app

# Install build dependencies (for compiling packages)
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    make \
    && apk add --no-cache libffi

# Copy dependency file and install dependencies into /install
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Copy application code
COPY britive_mcp_tools /app/britive_mcp_tools

FROM python:3.11-alpine

WORKDIR /app

# Install only required runtime libraries
RUN apk add --no-cache libffi && \
    rm -rf /var/cache/apk/*

# Copy Python packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY --from=builder /app/britive_mcp_tools /app/britive_mcp_tools

# Expose port
EXPOSE 5000

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1
    
# Start MCP server
CMD ["python", "britive_mcp_tools/core/mcp_runner.py"]
