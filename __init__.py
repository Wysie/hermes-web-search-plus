"""
web-search-plus — Hermes Plugin
Multi-provider web search with intelligent auto-routing.
Ported from robbyczgw-cla/web-search-plus-plugin (OpenClaw) to Hermes Plugin API.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

_SEARCH_SCRIPT = Path(__file__).parent / "search.py"


def _run_search(query: str, provider: str = "auto", count: int = 5, exa_depth: str = "normal") -> dict:
    """Call search.py subprocess and return parsed JSON result."""
    cmd = [
        sys.executable,
        str(_SEARCH_SCRIPT),
        "--query", query,
        "--provider", provider,
        "--max-results", str(count),
        "--compact",
    ]
    if exa_depth != "normal":
        cmd += ["--exa-depth", exa_depth]

    # Forward all relevant API keys from environment
    env = os.environ.copy()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=65,
            env=env,
        )
        if result.returncode != 0:
            stderr = result.stderr.strip()
            # Try to parse stderr as JSON (fallback/error output)
            try:
                return json.loads(stderr)
            except json.JSONDecodeError:
                return {"error": stderr or "Search failed", "provider": provider, "query": query, "results": []}

        return json.loads(result.stdout)

    except subprocess.TimeoutExpired:
        return {"error": "Search timed out after 30s", "provider": provider, "query": query, "results": []}
    except Exception as e:
        return {"error": str(e), "provider": provider, "query": query, "results": []}


def _format_results(data: dict) -> str:
    """Format search results for LLM consumption."""
    if "error" in data and not data.get("results"):
        return f"Search error: {data['error']}"

    results = data.get("results", [])
    provider = data.get("provider", "unknown")
    routing = data.get("routing", {})
    answer = data.get("answer", "")
    cached = data.get("cached", False)

    lines = []

    # Routing info
    if routing.get("auto_routed"):
        confidence = routing.get("confidence_level", "")
        reason = routing.get("reason", "")
        lines.append(f"[Provider: {provider} | auto-routed | {confidence} confidence | {reason}]")
    else:
        lines.append(f"[Provider: {provider}{' | cached' if cached else ''}]")

    # Direct answer if available
    if answer:
        lines.append(f"\nAnswer: {answer}\n")

    # Results
    for i, r in enumerate(results, 1):
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("snippet", "")
        lines.append(f"{i}. {title}")
        if url:
            lines.append(f"   {url}")
        if snippet:
            lines.append(f"   {snippet}")
        lines.append("")

    return "\n".join(lines).strip()


def register(ctx: Any) -> None:
    """Register web_search_plus tool with Hermes plugin system."""

    schema = {
        "name": "web_search_plus",
        "description": (
            "Multi-provider web search with intelligent auto-routing. "
            "Automatically selects the best provider based on query intent: "
            "Serper for shopping/news/facts, Tavily for research/analysis, "
            "Exa for semantic discovery, Querit for multilingual/real-time, "
            "Perplexity for direct answers. "
            "Override with provider param if needed."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query",
                },
                "provider": {
                    "type": "string",
                    "enum": ["auto", "serper", "tavily", "exa", "querit", "perplexity", "searxng"],
                    "description": "Search provider. Use 'auto' for intelligent routing (default).",
                    "default": "auto",
                },
                "depth": {
                    "type": "string",
                    "enum": ["normal", "deep", "deep-reasoning"],
                    "description": "Exa search depth: 'deep' synthesizes across sources (4-12s), 'deep-reasoning' for complex cross-document analysis (12-50s). Only applies when routed to Exa.",
                    "default": "normal",
                },
                "count": {
                    "type": "integer",
                    "description": "Number of results to return (default: 5)",
                    "default": 5,
                    "minimum": 1,
                    "maximum": 20,
                },
            },
            "required": ["query"],
        },
    }

    def handler(args_or_query, provider: str = "auto", count: int = 5, depth: str = "normal", **kwargs) -> str:
        # Hermes registry passes the entire input dict as first positional arg
        if isinstance(args_or_query, dict):
            query = args_or_query.get("query", "")
            provider = args_or_query.get("provider", provider)
            count = args_or_query.get("count", count)
            depth = args_or_query.get("depth", depth)
        else:
            query = args_or_query
        data = _run_search(query=query, provider=provider, count=count, exa_depth=depth)
        return _format_results(data)

    def check_fn() -> bool:
        """Plugin is available if at least one API key is configured."""
        keys = ["SERPER_API_KEY", "TAVILY_API_KEY", "EXA_API_KEY", "QUERIT_API_KEY"]
        return any(os.environ.get(k) for k in keys)

    ctx.register_tool(
        name="web_search_plus",
        toolset="web",
        schema=schema,
        handler=handler,
        check_fn=check_fn,
        requires_env=["SERPER_API_KEY"],
        description="Multi-provider web search with intelligent auto-routing",
        emoji="🔍",
    )
