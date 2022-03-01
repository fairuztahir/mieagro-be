const { createVuePlugin } = require('vite-plugin-vue2')
import path from 'path'

module.exports = {
  plugins: [createVuePlugin()],
  define: { 'process.env': {} },
  transpileDependencies: ['vuetify'],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  }
  // css: {
  //   loaderOptions: {
  //     sass: { additionalData: '@use "@/sass/overrides.sass" as *' },
  //     scss: { additionalData: '@use "@/sass/variables.scss" as *;' }
  //   }
  // }
}
