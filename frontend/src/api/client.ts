/**
 * The one API call the query console makes. Trimmed: see frontend/README.md.
 */
import type { FinancialQueryResponse } from "./types";

const ENDPOINT = "/api/retrieve/financial";

/** Mirrors the backend's `Field(min_length=3, max_length=500)`. */
export const QUERY_MIN_LENGTH = 3;
export const QUERY_MAX_LENGTH = 500;

export class FinancialApiError extends Error {
  readonly status: number | null;

  constructor(message: string, status: number | null = null) {
    super(message);
    this.name = "FinancialApiError";
    this.status = status;
  }
}

export async function askFinancialQuestion(
  query: string,
  signal?: AbortSignal,
): Promise<FinancialQueryResponse> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
    signal,
  });

  if (!response.ok) {
    // FastAPI returns `detail` as a string, or as a list of objects for a 422.
    // A 429 carries Retry-After: the concurrency ceiling refuses surplus work
    // rather than queueing it, so this is a "try shortly", not a failure.
    throw new FinancialApiError(await readErrorDetail(response), response.status);
  }

  return (await response.json()) as FinancialQueryResponse;
}
