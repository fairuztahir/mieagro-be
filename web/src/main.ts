import { createApp } from 'vue'
import vuetify from '@/plugins/vuetify'
import route from '@/routes'
import { createPinia } from 'pinia'
import App from './App.vue'

const store = createPinia()
const app = createApp(App)

// Assign Global
// app.config.globalProperties.pageTitle = 'Home1'

app.use(vuetify)
app.use(route)
app.use(store)
app.mount('#app')
