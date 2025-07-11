import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: [
      'fastfluence.home.lineofcode.pl',
      'localhost',
      '127.0.0.1'
    ]

  },
  // Build configuration
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})