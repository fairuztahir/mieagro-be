import { createApp } from 'vue'
import App from './App.vue'
import vuetify from '@/plugins/vuetify'
import route from '@/routes'
import store from '@/stores'

const app = createApp(App)

// Assign Global
// app.config.globalProperties.pageTitle = 'Home1'

app.use(vuetify)
app.use(store)
app.use(route)
app.mount('#app')
