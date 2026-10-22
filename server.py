import os
from openai import AsyncOpenAI
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Agent Router")

client = AsyncOpenAI(
    api_key=os.environ["AGENTROUTER_API_KEY"],
    base_url="https://co.agentrouter.org/v1",
)

@mcp.tool()
async def chat(message: str, model: str) -> str:
    """Send a message to Agent Router and return the AI response."""
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": message}],
    )
    return response.choices[0].message.content or ""

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
