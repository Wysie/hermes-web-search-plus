# web-search-plus — Hermes Plugin

Multi-provider web search with intelligent auto-routing as a native Hermes tool.

Ported from [web-search-plus-plugin](https://github.com/robbyczgw-cla/web-search-plus-plugin) (OpenClaw) to the [Hermes Agent](https://github.com/NousResearch/hermes-agent) plugin architecture.

## Features

- **Native Tool**: Registers `web_search_plus` directly in the Hermes tool registry
- **Intelligent Auto-Routing**: Picks the best provider based on query intent
- **Multi-Provider**: Serper, Tavily, Exa, Querit, Perplexity, You.com, SearXNG
- **Caching**: File-based cache to save API credits
- **Fallback**: Automatically tries next provider if one fails

## Supported Providers

| Provider | Best For | Free Tier | Auto-Route Trigger |
|---|---|---|---|
| **Serper** (Google) | Facts, news, shopping, local | 2,500/mo | "price", "buy", "news" |
| **Tavily** | Deep research, analysis | 1,000/mo | "how does", "explain" |
| **Exa** (Neural) | Semantic discovery, similarity | 1,000/mo | "similar to", "companies like" |
| **Querit** | Multilingual, real-time AI | 1,000/mo | Real-time info |
| **Perplexity** | AI-synthesized answers | Via API | Direct questions |
| **You.com** | Real-time RAG snippets | Limited | General RAG |
| **SearXNG** | Privacy, self-hosted | Free | Manual / fallback |

## Installation

1. Clone into your Hermes plugins directory:
   ```bash
   git clone https://github.com/robbyczgw-cla/hermes-web-search-plus ~/.hermes/plugins/web-search-plus
   ```

2. Configure API keys:
   ```bash
   cp .env.template .env
   # Edit .env and add at least one API key
   ```

3. Or set environment variables directly in `~/.hermes/.env`:
   ```
   SERPER_API_KEY=your-key
   TAVILY_API_KEY=your-key
   EXA_API_KEY=your-key
   ```

4. Restart Hermes — the plugin auto-loads from `~/.hermes/plugins/`.

5. Verify with `/plugins` in the Hermes CLI.

## Usage

The tool is available as `web_search_plus` in the agent:

```
web_search_plus(query="your query")                    # auto-route
web_search_plus(query="iPhone 16 price", provider="serper")
web_search_plus(query="how does HTTPS work", provider="tavily")
web_search_plus(query="startups like Notion", provider="exa")
```

## Plugin vs MCP

This plugin uses the native Hermes Plugin API (drop into `~/.hermes/plugins/`) rather than MCP. Benefits:
- No extra process spawning
- Direct tool registry integration
- Same API keys reused from `~/.hermes/.env`

## Architecture

```
~/.hermes/plugins/web-search-plus/
├── plugin.yaml      # Hermes plugin manifest
├── __init__.py      # register(ctx) — Hermes Plugin API entry point
├── search.py        # Core search logic (all providers, auto-routing, caching)
├── .env.template    # API key template (copy to .env)
└── .gitignore       # Keeps .env and cache out of git
```

## License

MIT
