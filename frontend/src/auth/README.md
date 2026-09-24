# frontend/src/auth

**Sign-in.** The UI reads `/health` to decide whether to render a sign-in screen, rather than probing an auth route that may not exist.

| | |
|---|---|
| `LoginPage.tsx` | the form |
| `session.ts` | token storage and the authenticated fetch wrapper |

_Implementations are private. This file lists what lives here and what it is responsible for._
