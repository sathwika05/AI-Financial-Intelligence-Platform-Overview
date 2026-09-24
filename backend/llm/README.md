# backend/llm

**Provider registry.** Models are not hardcoded. Providers and their models live in the database and the pipeline asks for a tier, not a model name. Keys are stored encrypted; nothing reads a provider key from the environment.

| | |
|---|---|
| `tiers.py` | the tier a caller asks for — **complete in this repo** |
| `llm_factory.py / llm_context.py` | client construction and per-run config |
| `llm_config_service.py` | provider and model resolution |
| `encryption_service.py` | Fernet encryption for stored keys |
| `message_text.py` | reads a reply as text whatever shape a provider returns |
| `usage_tracker.py` | tokens and cost per node |

_Implementations are private. This file lists what lives here and what it is responsible for._
