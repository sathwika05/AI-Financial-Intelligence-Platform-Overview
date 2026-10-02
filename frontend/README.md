# frontend

Vite + React + TypeScript. The API contract and how a query is made, alongside
the evaluation dashboard, admin screens and the component library behind them.

| File | What it shows |
|---|---|
| `src/api/types.ts` | the response contract, and where it is looser than it looks |
| `src/api/client.ts` | the one call, its error shapes and its length bounds |
| `src/components/QueryConsole.tsx` | the query screen and its states |
| `src/Root.tsx` | what the UI offers, decided by what the API mounts |
| `src/auth/`, `src/lib/`, `src/admin/`, `src/evaluation/` | see the README in each folder |

The UI calls the API through relative `/api` paths, never an absolute origin,
because the backend registers no CORS middleware. Every deployment therefore
serves both halves from one origin or rewrites `/api` and `/health` to the API;
local development uses a Vite dev proxy.

Screens are pictured in [the root README](../README.md#screens).
