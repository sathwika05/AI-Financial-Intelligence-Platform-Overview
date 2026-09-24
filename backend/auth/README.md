# backend/auth

**Authentication.** JWT with roles enforced per router. Mounted only in `full` mode.

| | |
|---|---|
| `passwords.py` | hashing and verification |
| `tokens.py` | issue and decode |
| `roles.py` | the role enum |
| `dependencies.py` | the FastAPI dependencies routers depend on |

_Implementations are private. This file lists what lives here and what it is responsible for._
