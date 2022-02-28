import Vue from 'vue'
import App from './App.vue'
import VueRouter from "vue-router";
import routes from "./routes/routes";

Vue.use(VueRouter);

// configure router
const router = new VueRouter({
  routes, // short for routes: routes
  scrollBehavior: (to) => {
    if (to.hash) {
      return { selector: to.hash };
    } else {
      return { x: 0, y: 0 };
    }
  },
  linkExactActiveClass: "nav-item active",
});

new Vue({
  render: (h) => h(App),
  router,
}).$mount('#app')
