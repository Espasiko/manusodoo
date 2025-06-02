import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3001,
    host: "0.0.0.0",
    strictPort: true,
    open: false,
    hmr: {
      overlay: false,
      clientPort: 3001,
      host: "localhost"
    },
    headers: {
      'X-Content-Type-Options': 'nosniff',
      'X-Frame-Options': 'DENY',
      'X-XSS-Protection': '1; mode=block'
    },
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        secure: false,
      },
    },
    allowedHosts: [
      "localhost",
      "3000-ishxvgs1vcbjdsxvwnkcc-72b27711.manusvm.computer",
      "3001-ishxvgs1vcbjdsxvwnkcc-72b27711.manusvm.computer"
    ]
  },
  build: {
    sourcemap: false,
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  }
});
