/**
 * Launching a run.
 *
 * The retrieval switches are per-run, which is what makes baseline, RRF,
 * cross-encoder and both comparable against the same questions.
 */
export interface RunRequest {
  providerId: string;
  questionSet: "valuation" | "growth" | "sentiment" | "mixed" | "smoke" | "focus" | "all";
  rrfEnabled: boolean;
  crossEncoderEnabled: boolean;
  /** null runs the ranker's default; 0 removes the model from the ranking. */
  llmBlendWeight: number | null;
}

export declare function RunBar(props: { onLaunch(request: RunRequest): void }): JSX.Element;
