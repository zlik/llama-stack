# Llama Stack Agent Framework

The Llama Stack agent framework is built on a modular architecture that allows for flexible and powerful AI applications. This document explains the key components and how they work together.

## Core Concepts

### 1. Agent Configuration

Agents are configured using the `AgentConfig` class, which includes:

- **Model**: The underlying LLM to power the agent
- **Instructions**: System prompt that defines the agent's behavior
- **Tools**: Capabilities the agent can use to interact with external systems
- **Safety Shields**: Guardrails to ensure responsible AI behavior

```python
from llama_stack_client import Agent


# Create the agent
agent = Agent(
    llama_stack_client,
    model="meta-llama/Llama-3-70b-chat",
    instructions="You are a helpful assistant that can use tools to answer questions.",
    tools=["builtin::code_interpreter", "builtin::rag/knowledge_search"],
)
```

### 2. Sessions

Agents maintain state through sessions, which represent a conversation thread:

```python
# Create a session
session_id = agent.create_session(session_name="My conversation")
```

### 3. Turns

Each interaction with an agent is called a "turn" and consists of:

- **Input Messages**: What the user sends to the agent
- **Steps**: The agent's internal processing (inference, tool execution, etc.)
- **Output Message**: The agent's response

```python
from llama_stack_client import AgentEventLogger

# Create a turn with streaming response
turn_response = agent.create_turn(
    session_id=session_id,
    messages=[{"role": "user", "content": "Tell me about Llama models"}],
)
for log in AgentEventLogger().log(turn_response):
    log.print()
```
###  Non-Streaming



```python
from rich.pretty import pprint

# Non-streaming API
response = agent.create_turn(
    session_id=session_id,
    messages=[{"role": "user", "content": "Tell me about Llama models"}],
    stream=False,
)
print("Inputs:")
pprint(response.input_messages)
print("Output:")
pprint(response.output_message.content)
print("Steps:")
pprint(response.steps)
```

### 4. Steps

Each turn consists of multiple steps that represent the agent's thought process:

- **Inference Steps**: The agent generating text responses
- **Tool Execution Steps**: The agent using tools to gather information
- **Shield Call Steps**: Safety checks being performed

## Agent Execution Loop


Refer to the [Agent Execution Loop](agent_execution_loop) for more details on what happens within an agent turn.
