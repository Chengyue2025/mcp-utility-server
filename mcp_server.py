```python
from fastmcp import FastMCP, Context
import requests
from datetime import datetime
import pytz
import ast
import operator
from typing import Optional

# Create MCP server
mcp = FastMCP("Utility Server")

# Tool 1: Web Fetch
@mcp.tool()
def web_fetch(url: str, ctx: Context) -> Optional[str]:
    """
    Fetch content from a webpage.
    
    Args:
        url: The URL to fetch content from
        ctx: MCP context
        
    Returns:
        Webpage content as text, or error message
    """
    try:
        ctx.info(f"Fetching URL: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text[:10000]  # Limit to 10000 chars
    except requests.exceptions.RequestException as e:
        error_msg = f"Error fetching URL: {str(e)}"
        ctx.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        ctx.error(error_msg)
        return error_msg


# Tool 2: Current Time
@mcp.tool()
def current_time(timezone: str = "UTC", ctx: Context = None) -> str:
    """
    Get current time in specified timezone.
    
    Args:
        timezone: Timezone string (e.g., 'America/New_York', 'Europe/London', 'Asia/Tokyo')
        ctx: MCP context
        
    Returns:
        Current time in the specified timezone
    """
    try:
        if timezone == "UTC":
            current = datetime.now(pytz.UTC)
        else:
            try:
                tz = pytz.timezone(timezone)
                current = datetime.now(tz)
            except pytz.exceptions.UnknownTimeZoneError:
                error_msg = f"Unknown timezone: {timezone}"
                if ctx:
                    ctx.error(error_msg)
                return error_msg
        
        formatted_time = current.strftime("%Y-%m-%d %H:%M:%S %Z")
        if ctx:
            ctx.info(f"Current time for {timezone}: {formatted_time}")
        return formatted_time
    except Exception as e:
        error_msg = f"Error getting time: {str(e)}"
        if ctx:
            ctx.error(error_msg)
        return error_msg


# Tool 3: Calculator
@mcp.tool()
def calculator(expression: str, ctx: Context) -> str:
    """
    Evaluate a mathematical expression.
    
    Args:
        expression: Mathematical expression (e.g., '2 + 2', '3 * (4 + 5)')
        ctx: MCP context
        
    Returns:
        Result of the expression
    """
    # Define allowed operators and operations
    allowed_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.Mod: operator.mod,
    }
    
    def safe_eval(node):
        if isinstance(node, ast.Expression):
            return safe_eval(node.body)
        elif isinstance(node, ast.Constant):
            return node.n if isinstance(node.n, (int, float)) else node.value
        elif isinstance(node, ast.BinOp):
            op_func = allowed_ops.get(type(node.op))
            if op_func is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            left = safe_eval(node.left)
            right = safe_eval(node.right)
            # Prevent division by zero
            if isinstance(node.op, ast.Div) and right == 0:
                raise ValueError("Division by zero")
            return op_func(left, right)
        elif isinstance(node, ast.UnaryOp):
            op_func = allowed_ops.get(type(node.op))
            if op_func is None:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            return op_func(safe_eval(node.operand))
        else:
            raise ValueError(f"Unsupported expression type: {type(node).__name__}")
    
    try:
        ctx.info(f"Evaluating expression: {expression}")
        parsed = ast.parse(expression.strip(), mode='eval')
        result = safe_eval(parsed.body)
        
        # Format result
        if isinstance(result, float):
            # For float results, limit decimal places
            result = round(result, 10)
            # Return as integer if it's a whole number
            if result == int(result):
                result = int(result)
        
        return str(result)
    
    except (SyntaxError, ValueError, ZeroDivisionError) as e:
        error_msg = f"Expression error: {str(e)}"
        ctx.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error in calculator: {str(e)}"
        ctx.error(error_msg)
        return error_msg


# Health check endpoint
@mcp.tool()
def health_check(ctx: Context) -> str:
    """Check if the server is running properly."""
    ctx.info("Health check performed")
    return "OK"


if __name__ == "__main__":
    mcp.run()
```