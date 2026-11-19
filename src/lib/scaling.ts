/** Klassen et al. (2022) scaling, as plotted in the Atlas: per-person production index,
 * normalised to 100 at a community of 100 people. Y = Y0·N^β ⇒ Y/N ∝ N^(β−1). */
export function perPersonIndex(n: number, beta: number): number {
  return 100 * Math.pow(n / 100, beta - 1)
}

export const KLASSEN_BETA = 1.227
export const KLASSEN_SE = 0.023
export const THEORY_BETA = 7 / 6
