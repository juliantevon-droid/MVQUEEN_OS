export type DatabaseProfile = "development" | "production";

export function databaseProfile(): DatabaseProfile {
  return process.env.MVQ_DATABASE_PROFILE === "production" ? "production" : "development";
}

export function assertDatabaseConfiguration(): void {
  const profile = databaseProfile();
  const url = process.env.DATABASE_URL?.trim() || "";

  if (!url) {
    throw new Error("DATABASE_URL is required.");
  }

  if (profile === "production") {
    if (!/^postgres(?:ql)?:\/\//i.test(url)) {
      throw new Error(
        "MVQ_DATABASE_PROFILE=production requires a PostgreSQL DATABASE_URL. File-based SQLite is not an approved production database.",
      );
    }
  } else if (!url.startsWith("file:")) {
    throw new Error(
      "Development database profile expects a file: SQLite DATABASE_URL. Use MVQ_DATABASE_PROFILE=production with the production Prisma schema for PostgreSQL.",
    );
  }
}
