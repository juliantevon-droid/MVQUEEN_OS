export function loginErrorMessage(errors: unknown) {
  if (!errors) return {};
  if (typeof errors === "object" && errors && "shop" in errors) {
    return errors as { shop?: string };
  }
  return { shop: "Unable to connect this Shopify store." };
}
