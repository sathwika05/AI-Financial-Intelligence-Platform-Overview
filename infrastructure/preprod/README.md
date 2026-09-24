# infrastructure/preprod

**Managed-host blueprint.** The public demo: one instance at 0.5 CPU and 512 MB, in `portfolio` mode. The UI is a separate static site that rewrites `/api` and `/health` to the API, keeping the browser same-origin — necessary because the backend mounts no CORS middleware.

| | |
|---|---|
| `render.yaml` | services, their sizes and the reasoning in comments |
| `vercel.json` | the rewrite rules for the static UI |

_Implementations are private. This file lists what lives here and what it is responsible for._
