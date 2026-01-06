### Building and Publishing (maintainers only)

```bash
# Increment version number (major|minor|patch)
uv version --bump minor

# Remove distributions for previous versions
rm -rf dist

# Build the package
uv build

# Publish to TestPyPI first (recommended)
uv publish --publish-url https://test.pypi.org/legacy/ --token pypi-YOUR_TEST_PYPI_TOKEN_HERE

# Test the deployment
For testing, add the following parameters to the `args` option in the claude_desktop_config.json.
  "args": [
    "--index-url",
    "https://test.pypi.org/simple/",
    "--extra-index-url",
    "https://pypi.org/simple/",
    "mcp-proto-okn"
  ]

# Publish to PyPI (production release)
uv publish --token pypi-YOUR_PYPI_TOKEN_HERE

# Clear uv cache (optional, if there are problems)
uv cache clean

# Remove cached tool installation (optional, if problems persist)
rm -rf ~/.local/share/uv/tools/mcp-proto-okn
```