import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'

// Dashboard pages
import DashboardLayout from '@/views/Dashboard/Layout/DashboardLayout.vue'
import Dashboard from '@/views/Dashboard/DashboardMain.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/dashboard',
    name: 'Home'
  },
  {
    path: '/',
    component: DashboardLayout,
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        components: { default: Dashboard }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
