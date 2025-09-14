# smoltest.py
# Try to use ollama

# file: agent_local.py
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel

# LiteLLM talks to your local Ollama server
model = LiteLLMModel(
    model_id="ollama_chat/qwen2.5:3b",   # or ollama_chat/llama3.1:8b
    api_base="http://localhost:11434"
)

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model,
)

print(agent.run("Find the altitude of Addis Ababa and return it as an integer in feet."))

