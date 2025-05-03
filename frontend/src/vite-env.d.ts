
// vite.config.ts
///<reference types="vite/client" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  
  server: {
    host: true,           // ← localhost だけでなく 0.0.0.0 でも Listen
    port: 5174,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        logLevel: "debug",
      },
    },
  },
  plugins: [react()],
});
