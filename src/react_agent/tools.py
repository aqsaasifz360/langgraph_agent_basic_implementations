"""This module provides example tools for web scraping and search functionality.

Includes a basic Tavily search function.

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

import os
from typing import Any, Callable, List, Optional, cast

from dotenv import load_dotenv
from langchain_tavily import TavilySearch  # type: ignore[import-not-found]

from react_agent.configuration import Configuration

# Load environment variables from .env
load_dotenv()

# Ensure the TAVILY_API_KEY is set
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in environment variables.")


async def search(query: str) -> Optional[dict[str, Any]]:
    """Search for general web results using Tavily.

    Tavily provides accurate and trustworthy web results for current events and more.
    """
    configuration = Configuration.from_context()
    wrapped = TavilySearch(
        tavily_api_key=TAVILY_API_KEY,
        max_results=configuration.max_search_results
    )
    return cast(dict[str, Any], await wrapped.ainvoke({"query": query}))


# This list is passed to LangChain tool-calling agents
TOOLS: List[Callable[..., Any]] = [search]
