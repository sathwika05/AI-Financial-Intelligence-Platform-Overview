/**
 * The query screen, trimmed to its states. See frontend/README.md.
 *
 * A pipeline run takes 10-45 seconds, which is long enough that the waiting
 * state is part of the design rather than a spinner.
 */
import { useState } from "react";

import { askFinancialQuestion, QUERY_MAX_LENGTH } from "../api/client";
import type { FinancialQueryResponse } from "../api/types";

export function QueryConsole() {
  const [query, setQuery] = useState("");
  const [report, setReport] = useState<FinancialQueryResponse | null>(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit() {
    setPending(true);
    setError(null);

    try {
      setReport(await askFinancialQuestion(query));
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Request failed");
    } finally {
      setPending(false);
    }
  }

  // A withheld report is rendered as its reason, never as an empty ranking:
  // telling a reader "0 unresolved issues" while withholding the reviewer's
  // result is worse than telling them nothing.
  return null;
}
