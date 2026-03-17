# Changelog

## [1.2.0] — 2026-03-17

### Added
- `depth` parameter for Exa deep research modes:
  - `deep`: multi-source synthesis (4-12s latency)
  - `deep-reasoning`: cross-document reasoning and analysis (12-50s latency)
- Timeout increased from 30s to 65s to support long-running deep-reasoning queries

### Fixed
- Handler now correctly unpacks input dict passed by Hermes registry (was causing "expected str, bytes or os.PathLike object, not dict" error on all calls)
- `depth` parameter name aligned with OpenClaw plugin v1.2.0 (was mistakenly named `exa_depth` in initial port)

### Notes
- Synced with [OpenClaw web-search-plus-plugin@908b145](https://github.com/robbyczgw-cla/web-search-plus-plugin/commit/908b14529230b1b300e44c6dd2cc8171833c1abb)

---

## [1.1.0] — 2026-03-17

### Fixed
- Plugin handler signature fixed: Hermes registry passes full input dict as first positional arg, not keyword args. Added `isinstance(args_or_query, dict)` check to unpack correctly.

---

## [1.0.0] — 2026-03-17

### Added
- Initial Hermes plugin port of web-search-plus from OpenClaw
- Auto-routing across Serper, Tavily, Exa, Querit, Perplexity, SearXNG
- `provider` parameter to force a specific provider
- `count` parameter for result count
- Hermes plugin registration via `register(ctx)` in `__init__.py`
