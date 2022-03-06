import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'

// Dashboard pages
import DashboardLayout from '@/views/Dashboard/Layout/DashboardLayout.vue'
import Dashboard from '@/views/Dashboard/DashboardMain.vue'

// Login
import LoginPage from '@/views/public/LoginPage.vue'

// Web
import Index from '@/views/public/Layout/WebLayout.vue'
import Home from '@/views/public/HomePage.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/home',
    component: Index,
    children: [
      {
        path: 'home',
        name: 'Home',
        components: { default: Home }
      },
      {
        path: 'login',
        name: 'Login',
        component: LoginPage
      }
    ]
  },
  {
    path: '/admin',
    redirect: '/admin/dashboard',
    component: DashboardLayout,
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
