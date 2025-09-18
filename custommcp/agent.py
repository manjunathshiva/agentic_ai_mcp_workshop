import os
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    SseConnectionParams
)

# Using the specified model
MODEL_NAME = "openai/gpt-oss-20b"

# Step 3 - Configure API Key
# Retrieve the API key from the userdata dictionary and set it as an environment variable for use in API client initialization

OPENAI_API_BASE="http://localhost:1234/v1"
OPENAI_API_KEY="anything"
os.environ["OPENAI_API_BASE"] = OPENAI_API_BASE
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


AGENT_MODEL = LiteLlm(
        model=MODEL_NAME,
        api_base=OPENAI_API_BASE,
        api_key=OPENAI_API_KEY
    )

toolset_greeting = MCPToolset(
        connection_params=SseConnectionParams(
            url="http://localhost:8100/mcp-server/mcp",
        )
    )

calculator_toolset = MCPToolset(
        connection_params=SseConnectionParams(
            url="http://localhost:8200/mcp-server/mcp",
        )
    )

root_agent = LlmAgent(
        model=AGENT_MODEL,
        name="assistant",
        instruction="""You are a helpful assistant that performs calculations.
        You have access to the following tools:
        - Greeting Tool
        - Calculator Tool
        Use the Greeting Tool to greet users.
        Use the Calculator Tool to perform calculations.
        Always call the appropriate tool for calculations and do not perform calculations yourself.
        Respond in a concise manner.
        """,
        tools=[toolset_greeting, calculator_toolset],
    )
