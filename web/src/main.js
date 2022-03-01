import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import routes from './routes/routes'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
// import 'vue-material/dist/theme/default.css'
// import 'vue-material/dist/theme/black-green-light.css'

Vue.use(VueRouter)
Vue.use(VueMaterial)

// configure router
const router = new VueRouter({
  routes, // short for routes: routes
  scrollBehavior: (to) => {
    if (to.hash) {
      return { selector: to.hash }
    } else {
      return { x: 0, y: 0 }
    }
  },
  linkExactActiveClass: 'nav-item active'
})

new Vue({
  render: (h) => h(App),
  router
}).$mount('#app')
