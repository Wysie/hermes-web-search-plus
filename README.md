# web-search-plus — Hermes Plugin

Multi-provider web search with intelligent auto-routing for [Hermes Agent](https://github.com/NousResearch/hermes-agent).

> Ported from [web-search-plus-plugin](https://github.com/robbyczgw-cla/web-search-plus-plugin) (OpenClaw) to the Hermes Plugin API.

---

## Quick Start

```bash
git clone https://github.com/robbyczgw-cla/hermes-web-search-plus.git ~/.hermes/plugins/web-search-plus
cd ~/.hermes/hermes-agent
source venv/bin/activate
cd ~/.hermes/plugins/web-search-plus
cp .env.template .env          # fill in at least one provider key
# Optional: pip install httpx  # only needed for Exa deep/deep-reasoning
```

Important:
- Use the Hermes virtualenv, not your system Python.
- Run `pip` only after `source ~/.hermes/hermes-agent/venv/bin/activate` (or from `~/.hermes/hermes-agent` via `source venv/bin/activate`).
- If you test the plugin from the CLI, prefer `~/.hermes/hermes-agent/venv/bin/python` or activate the Hermes venv first.

Then enable the plugin in `~/.hermes/config.yaml`:

```yaml
plugins:
  enabled:
    - web-search-plus
```

Finally restart Hermes (or `/restart` + `/reset` in gateway chats) and use `web_search_plus`.

---

## Features

- **Intelligent auto-routing** — picks the best provider based on query intent
- **7 providers** — Serper, Tavily, Exa, Querit, Perplexity, You.com, SearXNG
- **Exa Deep Research** — `depth=deep` for multi-source synthesis, `depth=deep-reasoning` for cross-document analysis
- **Adaptive fallback** — automatically skips providers on cooldown (1h after failure)
- **Routing transparency** — every response includes a `routing` object explaining provider choice
- **Time & domain filtering** — `time_range`, `include_domains`, `exclude_domains`
- **Local caching** — avoids duplicate API calls (1h TTL)

---

## Provider Routing

| Provider | Best for | Free tier |
|----------|----------|-----------|
| Serper (Google) | News, shopping, facts, local queries | 2,500/mo |
| Tavily | Research, deep content, academic | 1,000/mo |
| Exa | Semantic discovery, "alternatives to X", arxiv | 1,000/mo |
| Querit | Multilingual, real-time queries | 1,000/mo |
| Perplexity | Direct AI-synthesized answers | API key |
| You.com | LLM-ready real-time snippets | Limited |
| SearXNG | Privacy-focused, self-hosted, no API cost | Free |

Auto-routing scores providers based on query signals (keywords, intent, linguistic patterns). Every response includes a `routing` field explaining why a provider was chosen. Override anytime with `provider="serper"` etc.

---

## Installation

### API Keys

```bash
# Required (at least one)
SERPER_API_KEY=your-key        # https://serper.dev — 2,500 free/mo
TAVILY_API_KEY=your-key        # https://tavily.com — 1,000 free/mo
EXA_API_KEY=your-key           # https://exa.ai — 1,000 free/mo

# Optional
QUERIT_API_KEY=your-key        # https://querit.ai
PERPLEXITY_API_KEY=your-key    # https://perplexity.ai/settings/api
KILOCODE_API_KEY=your-key      # Perplexity via Kilo Gateway fallback
YOU_API_KEY=your-key           # https://api.you.com
SEARXNG_INSTANCE_URL=https://your-instance.example.com
```

> Python 3.8+ required. For Exa deep research: `pip install httpx` (optional).

---

## Usage

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | **required** | The search query |
| `provider` | string | `"auto"` | Force: `serper`, `tavily`, `exa`, `querit`, `perplexity`, `you`, `searxng` |
| `depth` | string | `"normal"` | Exa only: `normal`, `deep`, `deep-reasoning` |
| `count` | integer | `5` | Results (1–20) |
| `time_range` | string | — | `day`, `week`, `month`, `year` |
| `include_domains` | array | — | Whitelist: `["arxiv.org"]` |
| `exclude_domains` | array | — | Blacklist: `["reddit.com"]` |

### Examples

```python
web_search_plus(query="Graz weather today")
# → auto-routed to Serper (local/weather intent)

web_search_plus(query="alternatives to Notion", provider="exa")
# → Exa (discovery/similarity)

web_search_plus(query="LLM scaling laws research", provider="exa", depth="deep")
# → Exa deep synthesis (4–12s)

web_search_plus(query="OpenAI news", time_range="day")
# → Serper, last 24h

web_search_plus(query="LoRA fine-tuning", include_domains=["arxiv.org"])
# → arxiv only
```

### CLI testing

```bash
cd ~/.hermes/hermes-agent
source venv/bin/activate
python ~/.hermes/plugins/web-search-plus/search.py \
  --query "test query" --provider auto --max-results 5 --compact
```

---

## Architecture

```
__init__.py      — Hermes plugin entry, tool schema, handler
search.py        — Core engine: providers, routing, caching, fallback
plugin.yaml      — Plugin manifest
.env.template    — API key reference
CHANGELOG.md     — Version history
```

The plugin runs `search.py` as a subprocess with a 75s timeout (for Exa deep-reasoning queries).

---

## Related

- [web-search-plus-plugin](https://github.com/robbyczgw-cla/web-search-plus-plugin) — TypeScript version for OpenClaw
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) — the agent this plugin runs on
