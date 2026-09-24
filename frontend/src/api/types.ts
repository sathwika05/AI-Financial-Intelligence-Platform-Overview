/**
 * The response contract for POST /api/retrieve/financial.
 *
 * Modelled against real responses rather than the happy path. Two fields are
 * deliberately wider than they look:
 *
 *  - `marketCap` arrives as a number or as a preformatted string depending on
 *    which source supplied it.
 *  - `finalReport` may be withheld. A withheld report is not an error and not
 *    an empty report — it is the pipeline declining to present a ranking it
 *    could not have reviewed, and it carries the reason why.
 */

export type Intent = "VALUATION" | "GROWTH" | "SENTIMENT" | "MIXED" | "OUT_OF_SCOPE";

export type ReviewDecision =
  | "approved"
  | "forced_pass"
  | "withheld_review_unavailable"
  | "withheld_provider_unavailable";

export interface Citation {
  /** e.g. "NVDA-sql-1", "NVDA-vector-2" — the evidence a claim rests on. */
  citationId: string;
  source: "sql" | "vector" | "market" | "metrics";
  text: string;
}

export interface RankedCompany {
  ticker: string;
  name: string;
  rank: number;
  finalScore: number;
  /** Dimensions with no data are `null` — reported as unmeasured, not zero. */
  scores: Record<"valuation" | "growth" | "relevance" | "sentiment", number | null>;
  marketCap: number | string | null;
  evidence: Citation[];
}

export interface FinancialQueryResponse {
  query: string;
  finalReport: {
    intent: Intent;
    topCompanies: RankedCompany[];
    withheld?: boolean;
    review: { decision: ReviewDecision; flags: string[] };
  };
}
