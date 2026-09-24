# alembic

**Migrations.** 23 revisions. The chain begins by *altering* base tables, because those tables already existed when it started — so it cannot build a database from scratch. `startup_migration.py` decides whether to replay or stamp.

| | |
|---|---|
| `versions/` | the revisions |
| `env.py` | Alembic configuration |

_Implementations are private. This file lists what lives here and what it is responsible for._
