from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get the weather for a given city"""
    return f"The weather in {city} is sunny"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

#The transport=stdio allows the MCP server to communicate with the client over the standard input and output streams (stdin and stdout).
#This is the default transport for most MCP servers.
