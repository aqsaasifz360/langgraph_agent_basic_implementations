# src/react_agent/memory.py
from typing import List
from langchain_core.messages import BaseMessage

class SimpleMemory:
    def __init__(self):
        self.history: List[BaseMessage] = []

    def add_messages(self, messages: List[BaseMessage]):
        self.history.extend(messages)

    def get(self) -> List[BaseMessage]:
        return self.history
