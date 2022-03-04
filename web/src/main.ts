import { createApp } from 'vue'
import App from './App.vue'
import vuetify from '@/plugins/vuetify'
import routes from '@/routes'

const app = createApp(App)

// Assign Global
// app.config.globalProperties.pageTitle = 'Home1'

app.use(routes).use(vuetify).mount('#app')
