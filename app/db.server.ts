import { assertDatabaseConfiguration } from "./lib/enterprise/database-guard.server";
import prismaPackage from "@prisma/client";

const { PrismaClient } = prismaPackage;
type PrismaClientInstance = InstanceType<typeof PrismaClient>;

declare global {
  var prismaGlobal: PrismaClientInstance | undefined;
}

assertDatabaseConfiguration();

const prisma = globalThis.prismaGlobal ?? new PrismaClient();

if (process.env.NODE_ENV !== "production") {
  globalThis.prismaGlobal = prisma;
}

export default prisma;
