# MCP Utility Server

> A Python-based MCP (Model Context Protocol) server providing essential utility tools: web fetching, current time, and calculator functionality.

[![PyPI version](https://img.shields.io/pypi/v/mcp-utility-server.svg)](https://pypi.org/project/mcp-utility-server/)
[![npm version](https://img.shields.io/npm/v/mcp-utility-server.svg)](https://www.npmjs.com/package/mcp-utility-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)

## 🚀 Overview

`mcp-utility-server` is a lightweight, production-ready MCP server that exposes three powerful utility tools for AI assistants and LLM applications:

- **`web_fetch`** — Fetch and extract content from web pages
- **`current_time`** — Get the current time in any timezone
- **`calculator`** — Perform mathematical calculations with precision

Designed for seamless integration with MCP-compatible clients like Claude Desktop, VS Code Copilot, and custom LLM workflows.

---

## 📦 Installation

### Via pip (Recommended for Python projects)

```bash
pip install mcp-utility-server
```

### Via npm (For Node.js/TypeScript ecosystems)

```bash
npm install mcp-utility-server
```

### From source

```bash
git clone https://github.com/yourusername/mcp-utility-server.git
cd mcp-utility-server
pip install -e .
```

> **Note:** The npm package is a wrapper that bundles the Python server. Ensure Python 3.9+ is available on your system.

---

## 🧪 Quick Start

### 1. Configure your MCP client

Add this configuration to your MCP client (e.g., `~/.config/claude/claude_desktop_config.json` for Claude Desktop):

```json
{
  "mcpServers": {
    "utility": {
      "command": "mcp-utility-server",
      "args": []
    }
  }
}
```

Or if installed globally via npm:

```json
{
  "mcpServers": {
    "utility": {
      "command": "npx",
      "args": ["mcp-utility-server"]
    }
  }
}
```

### 2. Start using the tools

Once connected, your AI assistant can call these tools naturally:

```
"What's the current time in Tokyo?"
→ Calls current_time(timezone="Asia/Tokyo")

"Calculate 15% of €2,500"
→ Calls calculator(expression="2500 * 0.15")

"Fetch the content from https://example.com"
→ Calls web_fetch(url="https://example.com")
```

---

## 🛠️ API Reference

### Tool: `web_fetch`

Fetches the text content from a given URL.

**Parameters:**

| Parameter | Type   | Required | Default | Description                          |
|-----------|--------|----------|---------|--------------------------------------|
| `url`     | string | ✅ Yes    | —       | The URL to fetch (must include scheme, e.g., `https://`). |

**Returns:**  
`string` — The page title followed by the extracted text content (cleaned HTML-free text).

**Example:**

```json
{
  "input": {
    "url": "https://en.wikipedia.org/wiki/Python"
  },
  "output": "Python (programming language)\n\nPython is a high-level, general-purpose programming language..."
}
```

**Errors:** Returns an error message for invalid URLs, network issues, or non-200 responses.

---

### Tool: `current_time`

Returns the current date and time for a specified timezone.

**Parameters:**

| Parameter  | Type   | Required | Default   | Description                                                                 |
|------------|--------|----------|-----------|-----------------------------------------------------------------------------|
| `timezone` | string | ❌ No    | `"UTC"`   | A valid IANA timezone name (e.g., `"America/New_York"`, `"Asia/Kolkata"`). |

**Returns:**  
`string` — Formatted as `YYYY-MM-DD HH:MM:SS TZ` (e.g., `2025-03-15 14:30:00 EST`).

**Example:**

```json
{
  "input": {
    "timezone": "Europe/London"
  },
  "output": "2025-03-15 19:30:00 GMT"
}
```

**Errors:** Returns an error for invalid timezone names (use `pytz.all_timezones` for a complete list).

---

### Tool: `calculator`

Evaluates a mathematical expression with full operator support.

**Parameters:**

| Parameter    | Type   | Required | Default | Description                                           |
|--------------|--------|----------|---------|-------------------------------------------------------|
| `expression` | string | ✅ Yes    | —       | A mathematical expression (e.g., `"2 + 2 * 5"`).     |

**Supported operations:**  
`+`, `-`, `*`, `/`, `**` (power), `%` (modulo), parentheses, `pi`, `e`, `sqrt()`, `sin()`, `cos()`, `tan()`, `log()`, `abs()`, etc. (backed by `math` module).

**Returns:**  
`number` — The evaluated result (float or int).

**Example:**

```json
{
  "input": {
    "expression": "sin(pi/4) + log(100, 10)"
  },
  "output": 2.7071067811865475
}
```

**Errors:** Returns a clear error message for syntax errors, division by zero, or unsafe expressions (only mathematical operations allowed; no `__import__`, `exec`, or system calls).

---

## 🧰 Use Cases

- **Claude Desktop** — Give Claude web browsing, time awareness, and calculation capabilities
- **VS Code Copilot** — Enhance code suggestions with real-time data and computations
- **Custom LLM Agents** — Add utility tools to any MCP-compatible AI pipeline
- **Testing & Automation** — Use as a reliable, stateless utility service

---

## 🧑‍💻 Development

### Requirements

- Python 3.9+
- `mcp` package
- `httpx` (for HTTP requests)
- `pytz` (for timezone handling)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-utility-server.git
cd mcp-utility-server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

### Project Structure

```
mcp-utility-server/
├── src/
│   └── mcp_utility_server/
│       ├── __init__.py          # Package entry point
│       ├── server.py            # MCP server with tool definitions
│       └── tools/               # Tool implementations
│           ├── web_fetch.py
│           ├── current_time.py
│           └── calculator.py
├── tests/
│   └── test_tools.py
├── pyproject.toml               # Build configuration
├── package.json                  # npm wrapper
└── README.md                    # You are here
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/mcp_utility_server tests/
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure tests pass and coverage remains high.

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.

---

## 🙏 Acknowledgements

- Built on the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- Powered by [httpx](https://www.python-httpx.org/), [pytz](https://pythonhosted.org/pytz/), and Python's `math` module

---

**Made with ❤️ for the AI developer community**