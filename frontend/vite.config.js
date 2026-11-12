import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Skeleton config — extend proxy settings once backend routes are finalized.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
