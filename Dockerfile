# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

# Install uv for fast dependency resolution + build
RUN pip install --no-cache-dir uv

WORKDIR /build

# Copy only what is needed to install the package
# README.md is required by hatchling (declared as readme in pyproject.toml)
COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/
COPY config/ ./config/

# Build a wheel and install it (plus all deps) into an isolated prefix
RUN uv build --wheel --out-dir /dist \
 && uv pip install --system --no-cache \
      /dist/*.whl

# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

LABEL org.opencontainers.image.title="mcp-proto-okn" \
      org.opencontainers.image.description="MCP server for Proto-OKN SPARQL endpoints" \
      org.opencontainers.image.source="https://github.com/frink-okn/mcp-proto-okn"

# Install curl for the HEALTHCHECK (must use Host: localhost to satisfy
# the MCP SDK's TrustedHostMiddleware, which rejects pod-IP Host headers)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd --create-home --shell /bin/bash mcp

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin/mcp-proto-okn /usr/local/bin/mcp-proto-okn
COPY --from=builder /usr/local/bin/mcp-proto-okn-unified /usr/local/bin/mcp-proto-okn-unified

USER mcp
WORKDIR /home/mcp

# ── Configuration ──────────────────────────────────────────────────────────────
# Transport: streamable-http is the only sensible mode in a container
ENV MCP_PROTO_OKN_TRANSPORT=streamable-http \
    MCP_PROTO_OKN_HOST=0.0.0.0 \
    MCP_PROTO_OKN_PORT=8000 \
    # Trust forwarded headers from any upstream (ingress/gateway).
    # This disables uvicorn's TrustedHostMiddleware host-header check,
    # allowing requests proxied through nginx/traefik/gateway to pass through.
    UVICORN_FORWARDED_ALLOW_IPS="*"

# Optional – set via helm values / docker run -e:
#   MCP_PROTO_OKN_ENDPOINT   – SPARQL endpoint URL (required for single-endpoint mode)
#   MCP_PROTO_OKN_API_KEY    – Bearer-token auth (leave empty to disable)

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8000/mcp || exit 1

# Default: single-endpoint server.
# Override CMD in helm values to use 'mcp-proto-okn-unified' instead.
ENTRYPOINT ["mcp-proto-okn"]
CMD ["--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8000"]
