import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import styleImport, { VantResolve } from 'vite-plugin-style-import'

const path = require('path')

// https://vitejs.dev/config/
export default defineConfig({
  alias: {
    '@': path.resolve(__dirname, './src')
  },
  plugins: [
    vue(),
    styleImport({
      resolves: [VantResolve()],
    }),
  ],
  server: {
    host: '0.0.0.0'
  },
  define: {
    serverUrl: JSON.stringify('http://192.168.0.120:8001'),
    robotUrl: JSON.stringify('http://192.168.100.3:8000')
  }
})
