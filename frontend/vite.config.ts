import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Docker Compose のサービス名 network 経由で “backend:8000” にプロキシ
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,  // --host 相当
    proxy: {
      // /api/** へのリクエストは全て backend:8000/api/** に転送
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '/api'),
      },
      // JWT トークン取得も /api/token/ に叩く想定なら不要
      // '/api/token': {
      //   target: 'http://backend:8000',
      //   changeOrigin: true,
      // },
    },
  },
})
