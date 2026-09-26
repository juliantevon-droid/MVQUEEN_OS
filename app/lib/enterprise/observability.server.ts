import { randomUUID } from "node:crypto";

type LogLevel = "info" | "warn" | "error";
type Fields = Record<string, unknown>;

const SENSITIVE_KEY = /secret|token|password|authorization|cookie|api.?key|private.?key/i;

function sanitize(value: unknown, depth = 0): unknown {
  if (depth > 5) return "[max-depth]";
  if (Array.isArray(value)) return value.map((item) => sanitize(item, depth + 1));
  if (value && typeof value === "object") {
    const output: Record<string, unknown> = {};
    for (const [key, item] of Object.entries(value as Record<string, unknown>)) {
      output[key] = SENSITIVE_KEY.test(key) ? "[redacted]" : sanitize(item, depth + 1);
    }
    return output;
  }
  if (typeof value === "string" && value.length > 2000) return value.slice(0, 2000) + "…";
  return value;
}

export function createCorrelationId(prefix = "mvq"): string {
  return `${prefix}-${randomUUID()}`;
}

export function errorFields(error: unknown): Fields {
  if (error instanceof Error) {
    return { name: error.name, message: error.message, stack: error.stack };
  }
  return { message: String(error) };
}

export function logMvqueenEvent(
  event: string,
  fields: Fields = {},
  level: LogLevel = "info",
): void {
  const payload = sanitize({
    timestamp: new Date().toISOString(),
    system: "MVQUEEN_OS",
    event,
    ...fields,
  });
  const serialized = JSON.stringify(payload);
  if (level === "error") console.error(serialized);
  else if (level === "warn") console.warn(serialized);
  else console.info(serialized);
}
