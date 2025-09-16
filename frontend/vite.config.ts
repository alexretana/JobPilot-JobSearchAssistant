import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import solidPlugin from "vite-plugin-solid";

export default defineConfig({
  plugins: [tailwindcss(), solidPlugin()],
  server: {
    port: 3000,
    proxy: {
      // Proxy all API routes to the backend
      // This will match any path that starts with the router prefixes
      '^/(jobs|users|auth|companies|applications|resumes|skill_banks|timeline|job_sources|search|job_deduplication|stats)/.*': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      // Also proxy the root-level API endpoints
      '^/(health|test-auth-setting|test-token)': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  build: {
    target: "esnext",
  },
});
