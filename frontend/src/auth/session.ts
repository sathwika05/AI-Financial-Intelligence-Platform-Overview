/**
 * Token storage and the authenticated fetch wrapper.
 *
 * The UI reads `/health` to decide whether to render a sign-in screen at all,
 * rather than probing an auth route that may not be mounted — in `portfolio`
 * mode the auth router does not exist, and a 404 is not a sign-in prompt.
 */
export interface Session {
  token: string;
  email: string;
  role: "viewer" | "analyst" | "admin";
}

/** Whether this deployment mounts auth at all. Read once, at boot. */
export declare function authRequired(): Promise<boolean>;

export declare function currentSession(): Session | null;

/** fetch(), with the bearer token attached and a 401 clearing the session. */
export declare function withAuth(input: RequestInfo, init?: RequestInit): Promise<Response>;
