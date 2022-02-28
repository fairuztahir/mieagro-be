const { createVuePlugin } = require('vite-plugin-vue2')
import path from 'path'

module.exports = {
  plugins: [createVuePlugin()],
  define: { 'process.env': {} },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
}
