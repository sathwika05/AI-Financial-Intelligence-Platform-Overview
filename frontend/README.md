# frontend — minimal excerpt

Vite + React + TypeScript. Enough to show the API contract and how a query is
made; the rest of the UI — the evaluation dashboard, admin screens and the
component library behind them — is private.

| File | What it shows |
|---|---|
| `src/api/types.ts` | the response contract, and where it is looser than it looks |
| `src/api/client.ts` | the one call, its error shapes and its length bounds |
| `src/components/QueryConsole.tsx` | the query screen, trimmed to its states |

The UI calls the API through relative `/api` paths, never an absolute origin,
because the backend registers no CORS middleware. Every deployment therefore
serves both halves from one origin or rewrites `/api` and `/health` to the API;
local development uses a Vite dev proxy.

Screens are pictured in [the root README](../README.md#screens).
