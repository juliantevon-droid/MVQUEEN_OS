import { reactRouter } from "@react-router/dev/vite";
import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";

const host = new URL(process.env.SHOPIFY_APP_URL || "http://localhost").hostname;

export default defineConfig({
  server:{allowedHosts:[host],port:Number(process.env.PORT || 3000)},
  plugins:[reactRouter(),tsconfigPaths()],
});
