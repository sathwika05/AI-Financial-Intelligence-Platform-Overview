/**
 * Display formatting.
 *
 * Market capitalisation arrives as a number or as a preformatted string
 * depending on which source supplied it, so every formatter here accepts both
 * rather than asserting one.
 *
 * Illustrative excerpt — signatures and contracts only. Bodies are elided and
 * the imports do not resolve, so this file does not build.
 */
export declare function formatMarketCap(value: number | string | null): string;

export declare function formatRatio(value: number | null): string;

/** A dimension with no data reads as "unmeasured", never as zero. */
export declare function formatScore(value: number | null): string;

export declare function formatLatency(ms: number): string;
