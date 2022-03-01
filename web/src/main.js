import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import routes from '@/routes'
import vuetify from '@/plugins/vuetify'

Vue.config.productionTip = false
Vue.use(VueRouter)

// configure router
const router = new VueRouter({
  routes
  // scrollBehavior: (to) => {
  //   if (to.hash) {
  //     return { selector: to.hash }
  //   } else {
  //     return { x: 0, y: 0 }
  //   }
  // },
  // linkExactActiveClass: 'nav-item active'
})

new Vue({
  router,
  vuetify,
  render: (h) => h(App)
}).$mount('#app')
