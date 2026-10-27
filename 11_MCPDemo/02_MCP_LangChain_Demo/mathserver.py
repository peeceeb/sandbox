from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> int:
    return a / b

if __name__ == "__main__":
    mcp.run(transport="stdio")

#The transport=stdio allows the MCP server to communicate with the client over the standard input and output streams (stdin and stdout).
#This is the default transport for most MCP servers.

