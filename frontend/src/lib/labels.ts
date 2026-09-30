/**
 * The vocabulary shown to a reader.
 *
 * Recommendation buckets are deliberately coarse. A finer scale would imply a
 * precision the composite score does not have.
 *
 * Illustrative excerpt — signatures and contracts only. Bodies are elided and
 * the imports do not resolve, so this file does not build.
 */
export type Recommendation =
  | "Strong Buy" | "Buy" | "Hold" | "Sell" | "Strong Sell";

export declare function recommendationFor(finalScore: number): Recommendation;

/** Why an answer was withheld, in words a reader can act on. */
export declare function withheldReason(decision: string): string;
