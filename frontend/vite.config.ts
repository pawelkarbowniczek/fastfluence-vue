import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    // Usunięto proxy - używamy bezpośrednich domen
  },
  // Build configuration
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})