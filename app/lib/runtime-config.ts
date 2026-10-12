/** Read bounded worker settings without treating an unset value as zero. */
export function envInt(name: string, fallback: number, min: number, max: number): number {
  const value = process.env[name]?.trim();
  if (!value) return fallback;
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) return fallback;
  return Math.max(min, Math.min(max, Math.floor(parsed)));
}
