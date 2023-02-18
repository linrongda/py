import { defineConfig } from 'vite'
import { resolve } from "path";
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {                
    host: '0.0.0.0'    // host改为0.0.0.0，内网可用
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, "./src"),
    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        // 两种方式都可以
        // additionalData: '@use "@/assets/scss/global.scss" as *;'
      }
    }
  }
})
