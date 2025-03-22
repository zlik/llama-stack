## Agent Execution Loop

Agents are the heart of complex AI applications. They combine inference, memory, safety, and tool usage into coherent workflows. At its core, an agent follows a sophisticated execution loop that enables multi-step reasoning, tool usage, and safety checks.

Each agent turn follows these key steps:

1. **Initial Safety Check**: The user's input is first screened through configured safety shields

2. **Context Retrieval**:
   - If RAG is enabled, the agent can choose to query relevant documents from memory banks. You can use the `instructions` field to steer the agent.
   - For new documents, they are first inserted into the memory bank.
   - Retrieved context is provided to the LLM as a tool response in the message history.

3. **Inference Loop**: The agent enters its main execution loop:
   - The LLM receives a user prompt (with previous tool outputs)
   - The LLM generates a response, potentially with [tool calls](tools)
   - If tool calls are present:
     - Tool inputs are safety-checked
     - Tools are executed (e.g., web search, code execution)
     - Tool responses are fed back to the LLM for synthesis
   - The loop continues until:
     - The LLM provides a final response without tool calls
     - Maximum iterations are reached
     - Token limit is exceeded

4. **Final Safety Check**: The agent's final response is screened through safety shields

```{mermaid}
sequenceDiagram
    participant U as User
    participant E as Executor
    participant M as Memory Bank
    participant L as LLM
    participant T as Tools
    participant S as Safety Shield

    Note over U,S: Agent Turn Start
    U->>S: 1. Submit Prompt
    activate S
    S->>E: Input Safety Check
    deactivate S

    loop Inference Loop
        E->>L: 2.1 Augment with Context
        L-->>E: 2.2 Response (with/without tool calls)

        alt Has Tool Calls
            E->>S: Check Tool Input
            S->>T: 3.1 Execute Tool
            T-->>E: 3.2 Tool Response
            E->>L: 4.1 Tool Response
            L-->>E: 4.2 Synthesized Response
        end

        opt Stop Conditions
            Note over E: Break if:
            Note over E: - No tool calls
            Note over E: - Max iterations reached
            Note over E: - Token limit exceeded
        end
    end

    E->>S: Output Safety Check
    S->>U: 5. Final Response
```

Each step in this process can be monitored and controlled through configurations. Here's an example that demonstrates monitoring the agent's execution:

```python
from llama_stack_client import LlamaStackClient, Agent, AgentEventLogger
from rich.pretty import pprint

# Replace host and port
client = LlamaStackClient(base_url=f"http://{HOST}:{PORT}")

agent = Agent(
    client,
    # Check with `llama-stack-client models list`
    model="Llama3.2-3B-Instruct",
    instructions="You are a helpful assistant",
    # Enable both RAG and tool usage
    tools=[
        {
            "name": "builtin::rag/knowledge_search",
            "args": {"vector_db_ids": ["my_docs"]},
        },
        "builtin::code_interpreter",
    ],
    # Configure safety (optional)
    input_shields=["llama_guard"],
    output_shields=["llama_guard"],
    # Control the inference loop
    max_infer_iters=5,
    sampling_params={
        "strategy": {"type": "top_p", "temperature": 0.7, "top_p": 0.95},
        "max_tokens": 2048,
    },
)
session_id = agent.create_session("monitored_session")

# Stream the agent's execution steps
response = agent.create_turn(
    messages=[{"role": "user", "content": "Analyze this code and run it"}],
    documents=[
        {
            "content": "https://raw.githubusercontent.com/example/code.py",
            "mime_type": "text/plain",
        }
    ],
    session_id=session_id,
)

# Monitor each step of execution
for log in AgentEventLogger().log(response):
    log.print()

# Using non-streaming API, the response contains input, steps, and output.
response = agent.create_turn(
    messages=[{"role": "user", "content": "Analyze this code and run it"}],
    documents=[
        {
            "content": "https://raw.githubusercontent.com/example/code.py",
            "mime_type": "text/plain",
        }
    ],
    session_id=session_id,
)

pprint(f"Input: {response.input_messages}")
pprint(f"Output: {response.output_message.content}")
pprint(f"Steps: {response.steps}")
```
