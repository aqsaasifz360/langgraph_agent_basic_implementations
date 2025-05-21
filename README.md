
# LangGraph ReAct Agent – Gemini Edition

This project is a customized ReAct agent built with [LangGraph](https://github.com/langchain-ai/react-agent.git) that uses:

- **Google Gemini** models via **Vertex AI**
- **Tavily** for live web search
- **Human-in-the-loop (HITL)** interaction
- **In-memory message history (Memory)**
- Extensible tool-calling architecture
- Built to run in **LangGraph Studio** with debugging and time travel features

![Graph view in LangGraph studio UI](./static/studio_ui_output.JPG)

---

## What It Does

The ReAct agent:

1. Accepts a user query
2. Reasons over context and prior memory
3. Invokes external tools (e.g., Tavily Search) if needed
4. Triggers human-in-the-loop review. Human can edit the responses.
5. Stores all interactions in memory
6. Returns a structured response

---

## 🛠️ Technologies Used

| Feature               | Implementation                                    |
|----------------------|---------------------------------------------------|
| LLM Backend           | Google Gemini via Vertex AI (`gemini-2.0-flash`) |
| Tooling               | Tavily Search API                                 |
| Memory                | In-memory message storage                         |
| HITL                  | CLI-based human override                          |
| Agent Pattern         | ReAct loop using LangGraph                        |
| IDE                   | LangGraph Studio                                  |

---

## Getting Started

### 1. Clone and Set Up Environment

```bash
git clone <your-repo-url>
cd react-agent
cp .env.example .env
```

### 2. Update Your `.env`

```env
GOOGLE_APPLICATION_CREDENTIALS=path/to/service_account.json
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
TAVILY_API_KEY=your-tavily-key
```

Ensure your JSON file has the correct scopes:

```python
["https://www.googleapis.com/auth/generative-language"]
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Agent

You can run the agent via a Python script like:

```bash
python main.py
```

### Example conversation:

```text
User: What's the capital of France?
Assistant: The capital of France is Paris.

User: Can edit the responses
Your input or correction: Actually, it's Lyon.
Assistant: Got it.
```

---

## Features You Can Customize

| Feature           | How to Customize                                    |
|------------------|-----------------------------------------------------|
| **Prompt**       | `prompts.py` (system prompt format)                 |
| **Model**        | Set in `.env` or `google_model.py`                  |
| **Tools**        | Modify `tools.py`                                   |
| **HITL Trigger** | Change keyword in `graph.py → route_model_output()` |
| **Memory**       | Replace `SimpleMemory` with a persistent store      |

---

## Studio Support

This project supports **LangGraph Studio** for:

- Graph visualization
- State introspection
- Time travel (re-run from any node)

To launch studio:

```bash
langgraph studio
```

---

## Key files used

```bash
src/react_agent/
│
├── graph.py              # Main agent loop + logic
├── tools.py              # Tavily tool integration
├── prompts.py            # System prompt
├── state.py              # Input/output schema
├── configuration.py      # LangGraph config schema
├── google_model.py       # Gemini model loader via Vertex AI
├── memory.py             # Simple in-memory store
└── utils.py              # Optional helpers (e.g. for loading models)
```

---
