import { createApp } from 'vue'
import App from './App.vue'
import vuetify from '@/plugins/vuetify'
import routes from '@/routes'
// import { loadFonts } from './plugins/webfontloader'

const app = createApp(App)
// loadFonts()

// Assign Global
// app.config.globalProperties.pageTitle = 'Home1'

app.use(routes).use(vuetify).mount('#app')
