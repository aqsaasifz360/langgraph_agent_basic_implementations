"""Define a custom Reasoning and Action agent.

Works with a chat model with tool calling support.
"""

from datetime import UTC, datetime
from typing import Dict, List, Literal, cast

from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from react_agent.configuration import Configuration
from react_agent.state import InputState, State
from react_agent.tools import TOOLS
from react_agent.utils import load_chat_model
from src.react_agent.google_model import llm
from react_agent.memory import SimpleMemory
from langchain_core.messages import AIMessage, HumanMessage

memory = SimpleMemory()



# Define the function that calls the model

async def human_review(state: State) -> Dict[str, List[AIMessage]]:
    print("\n[HUMAN REVIEW TRIGGERED]")
    print("Model Output:", state.messages[-1].content)
    user_input = input("Your input or correction: ")
    return {"messages": [HumanMessage(content=user_input)]}


async def call_model(state: State) -> Dict[str, List[AIMessage]]:
    configuration = Configuration.from_context()
    model = llm.bind_tools(TOOLS)
    system_message = configuration.system_prompt.format(
        system_time=datetime.now(tz=UTC).isoformat()
    )

    # Get memory
    past_messages = memory.get()
    full_prompt = [{"role": "system", "content": system_message}] + past_messages + state.messages

    response = cast(
        AIMessage,
        await model.ainvoke(full_prompt),
    )

    # Save messages to memory
    memory.add_messages(state.messages)
    memory.add_messages([response])

    if state.is_last_step and response.tool_calls:
        return {
            "messages": [AIMessage(
                id=response.id,
                content="Sorry, I could not find an answer in the allowed steps.",
            )]
        }

    return {"messages": [response]}



# Define a new graph

builder = StateGraph(State, input=InputState, config_schema=Configuration)

# Define the two nodes we will cycle between
builder.add_node(call_model)
builder.add_node("tools", ToolNode(TOOLS))

# Set the entrypoint as `call_model`
# This means that this node is the first one called
builder.add_edge("__start__", "call_model")


def route_model_output(state: State) -> Literal["__end__", "tools", "human"]:
    last_message = state.messages[-1]
    if not isinstance(last_message, AIMessage):
        raise ValueError("Expected AIMessage")

    # Manual keyword trigger (customize as needed)
    if "HUMAN_REVIEW" in last_message.content.upper():
        return "human"

    if last_message.tool_calls:
        return "tools"

    return "__end__"



# Add a conditional edge to determine the next step after `call_model`
builder.add_conditional_edges(
    "call_model",
    # After call_model finishes running, the next node(s) are scheduled
    # based on the output from route_model_output
    route_model_output,
)

# Add a normal edge from `tools` to `call_model`
# This creates a cycle: after using tools, we always return to the model
builder.add_edge("tools", "call_model")
builder.add_node("human", human_review)
builder.add_edge("tools", "call_model")
builder.add_edge("human", "call_model")

# Compile the builder into an executable graph
graph = builder.compile(name="ReAct Agent")