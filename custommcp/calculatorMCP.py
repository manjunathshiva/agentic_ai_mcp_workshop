from fastmcp import FastMCP
from fastapi import FastAPI
from starlette.routing import Mount
import uvicorn

# Create your FastMCP server as well as any tools, resources, etc.
mcp = FastMCP("CalculatorServer")
@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """
    Adds two numbers.
    Args:
        a: The first number.
        b: The second number.
    Returns:
        The sum of the two numbers.
    """
    return a + b

@mcp.tool()
def subtract_numbers(a: float, b: float) -> float:
    """
    Subtracts the second number from the first number.
    Args:
        a: The first number.
        b: The second number.
    Returns:
        The result of subtracting b from a.
    """
    return a - b

@mcp.tool()
def multiply_numbers(a: float, b: float) -> float:
    """
    Multiplies two numbers.
    Args:
        a: The first number.
        b: The second number.
    Returns:
        The product of the two numbers.
    """
    return a * b

@mcp.tool()
def divide_numbers(a: float, b: float) -> float:
    """
    Divides the first number by the second number.
    Args:
        a: The numerator.
        b: The denominator.
    Returns:
        The result of dividing a by b.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

# Create the ASGI app for FastMCP with SSE transport
mcp_app = mcp.http_app(path='/mcp', transport="sse")
# Create a FastAPI app and mount the MCP server
app = FastAPI(lifespan=mcp_app.lifespan)
app.mount("/mcp-server", mcp_app)

if __name__ == "__main__":
    uvicorn.run("calculatorMCP:app", host="0.0.0.0", port=8200, reload=True)
# Run with: uvicorn calculatorMCP:app --host 0.0.0.0 --port=8200 --reload