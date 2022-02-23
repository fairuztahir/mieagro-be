import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
// import HomeView from '../views/HomeView.vue';
import HelloWorld from '@/views/HelloWorld2.vue'
import Test from '@/views/dashboard/Index.vue'
import PageNotFound from '@/views/PageNotFound.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: HelloWorld
  },
  {
    path: '/test',
    name: 'Test',
    component: Test
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'PageNotFound',
    component: PageNotFound
  }
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue'),
  // },
  // {
  //   path: '/vuetify',
  //   name: 'vuetify',
  //   component: HelloWorld,
  // },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
