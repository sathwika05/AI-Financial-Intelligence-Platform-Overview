/**
 * The run summary — the screen pictured in the root README.
 *
 * Every headline metric carries its delta against the previous run, because a
 * single run's number means little against an 11-question noise floor.
 *
 * Illustrative excerpt — signatures and contracts only. Bodies are elided and
 * the imports do not resolve, so this file does not build.
 */
export interface RunSummary {
  runId: string;
  status: "queued" | "running" | "completed" | "failed" | "cancelled";
  questionSet: string;
  provider: string;
  passRate: number;
  routeAccuracy: number;
  faithfulness: number | null;
  contextPrecision: number | null;
  /** Which retrieval stages this run actually used, not what was requested. */
  retrieval: { rrf: boolean; crossEncoder: boolean };
}

export declare function SummaryView(props: { runId: string }): JSX.Element;
