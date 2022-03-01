import { createApp } from 'vue'
import App from './App.vue'
import vuetify from '@/plugins/vuetify'
import routes from '@/routes'
import { loadFonts } from './plugins/webfontloader'

loadFonts()

createApp(App).use(routes).use(vuetify).mount('#app')
