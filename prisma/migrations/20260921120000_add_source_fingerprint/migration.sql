-- Add source fingerprinting so identical source product events become safe no-ops.
ALTER TABLE "ProductAutomationState" ADD COLUMN "sourceFingerprint" TEXT;
