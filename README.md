# web-search-plus — Hermes Plugin

Multi-provider web search with intelligent auto-routing for the Hermes AI agent.

Ported from [robbyczgw-cla/web-search-plus-plugin](https://github.com/robbyczgw-cla/web-search-plus-plugin) (OpenClaw) to the Hermes Plugin API.

---

## Features

- **Auto-routing**: Automatically picks the best provider based on query intent
- **Multiple providers**: Serper, Tavily, Exa, Querit, Perplexity, SearXNG
- **Exa Deep Research**: `depth=deep` for multi-source synthesis, `depth=deep-reasoning` for cross-document analysis
- **Caching**: Avoids duplicate API calls for repeated queries
- **Compact output**: Formatted for LLM consumption

## Routing Logic

| Provider | Best for |
|----------|----------|
| Serper (Google) | News, shopping, facts, local queries |
| Tavily | Research, deep content, academic topics |
| Exa | Semantic discovery, "alternatives to X", "companies like Y", arxiv |
| Querit | Multilingual, real-time queries |
| Perplexity | Direct answers |

Auto-routing scores each provider based on query signals and picks the highest-confidence match. You can always override with `provider=...`.

---

## Installation

The plugin is loaded automatically by Hermes from `~/.hermes/plugins/web-search-plus/`.

### API Keys

Set in your environment or `~/.hermes/plugins/web-search-plus/.env`:

```bash
# Required (at least one)
SERPER_API_KEY=...       # https://serper.dev
TAVILY_API_KEY=...       # https://tavily.com
EXA_API_KEY=...          # https://exa.ai

# Optional
QUERIT_API_KEY=...       # https://querit.ai
PERPLEXITY_API_KEY=...   # https://www.perplexity.ai/settings/api
KILOCODE_API_KEY=...     # fallback for Perplexity via Kilo Gateway
YOU_API_KEY=...          # https://api.you.com
SEARXNG_INSTANCE_URL=... # self-hosted SearXNG instance
```

---

## Tool: `web_search_plus`

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | required | The search query |
| `provider` | string | `"auto"` | Force a provider: `serper`, `tavily`, `exa`, `querit`, `perplexity`, `searxng`, or `auto` |
| `depth` | string | `"normal"` | Exa depth mode: `normal`, `deep` (4-12s), `deep-reasoning` (12-50s) |
| `count` | integer | `5` | Number of results (1-20) |

### Examples

```
# Auto-routing (default)
web_search_plus(query="Graz weather today")

# Force Exa for semantic discovery
web_search_plus(query="alternatives to Notion", provider="exa")

# Exa deep research
web_search_plus(query="impact of LLMs on software development", provider="exa", depth="deep")

# Exa deep reasoning for complex analysis
web_search_plus(query="reconcile conflicting claims about transformer scaling laws", provider="exa", depth="deep-reasoning")

# Force Serper for news
web_search_plus(query="OpenAI latest news", provider="serper")
```

---

## Hermes Plugin API Notes

The Hermes registry calls handlers with the full input dict as the first positional argument (not as `**kwargs`). The handler in `__init__.py` accounts for this by checking `isinstance(args_or_query, dict)` and unpacking accordingly.

Timeout is set to **65 seconds** to accommodate Exa deep-reasoning queries which can take 12-50s.

---

## Architecture

```
__init__.py          — Hermes plugin entry point, tool registration, handler
search.py            — Core search engine (all providers, routing logic, ~2600 lines)
plugin.yaml          — Plugin manifest (name, version, toolsets)
.env.template        — API key template
```

The plugin calls `search.py` as a subprocess, passing query parameters as CLI args and forwarding all env vars.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

---

## Related

- [OpenClaw plugin](https://github.com/robbyczgw-cla/web-search-plus-plugin) — original TypeScript version for OpenClaw
- Hermes repo: `robbyczgw-cla/hermes-web-search-plus`
