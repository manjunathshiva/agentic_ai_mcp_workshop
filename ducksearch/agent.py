import os
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioServerParameters,
    StdioConnectionParams
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

toolset = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command='',
                    args=[""],
                ),
            timeout=15,
        )
    )

root_agent = LlmAgent(
        model=AGENT_MODEL,
        name="assistant",
        instruction="""
       
        """,
        tools=[toolset],
    )
