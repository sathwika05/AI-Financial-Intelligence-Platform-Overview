/**
 * Provider and model configuration.
 *
 * Keys are write-only from here: the UI can set one and can see that one is
 * set, but never reads it back. What is stored is encrypted at rest.
 *
 * Illustrative excerpt — signatures and contracts only. Bodies are elided and
 * the imports do not resolve, so this file does not build.
 */
export interface ProviderRow {
  id: string;
  name: string;
  isDefault: boolean;
  connectionStatus: "untested" | "ok" | "failed";
  /** Never the key itself. */
  hasKey: boolean;
  models: { tier: "small" | "medium" | "large"; model: string }[];
}

export declare function ProvidersScreen(): JSX.Element;
