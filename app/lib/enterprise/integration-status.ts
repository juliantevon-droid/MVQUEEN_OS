export type IntegrationState = "connected" | "configured_disabled" | "not_connected";

export type IntegrationStatus = {
  provider: string | null;
  state: IntegrationState;
  executionEnabled: boolean;
};

function status(providerEnv: string, enabledEnv: string): IntegrationStatus {
  const provider = process.env[providerEnv]?.trim() || null;
  const requested = process.env[enabledEnv] === "true";
  if (!provider) return { provider: null, state: "not_connected", executionEnabled: false };
  if (!requested) return { provider, state: "configured_disabled", executionEnabled: false };
  return { provider, state: "connected", executionEnabled: true };
}

export function getEnterpriseIntegrationStatus() {
  return {
    paidMedia: status("MVQ_AD_PROVIDER", "MVQ_AD_EXECUTION_ENABLED"),
    analytics: status("MVQ_ANALYTICS_PROVIDER", "MVQ_ANALYTICS_EXPORT_ENABLED"),
    lifecycle: status("MVQ_LIFECYCLE_PROVIDER", "MVQ_LIFECYCLE_EXECUTION_ENABLED"),
  };
}
