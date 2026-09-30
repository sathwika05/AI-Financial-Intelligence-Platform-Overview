/**
 * Application root.
 *
 * Which screens exist depends on the deployment: `/health` reports whether
 * auth is required, and in `portfolio` mode the admin and evaluation routes
 * are not mounted on the API at all, so the UI does not offer them.
 */

export interface Health {
  status: "ok" | "degraded";
  db: "connected" | "error";
  /** Not fatal. Every caller of the cache fails open. */
  redis: "connected" | "error";
  authRequired: boolean;
}

export declare function Root(): JSX.Element;
