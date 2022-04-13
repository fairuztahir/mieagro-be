import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import { useAuth } from '@/services/auth'

// Dashboard pages
import DashboardLayout from '@/views/Dashboard/Layout/DashboardLayout.vue'
import Dashboard from '@/views/Dashboard/DashboardMain.vue'
import Table from '@/views/Dashboard/TablePage.vue'
import Icon from '@/views/Dashboard/IconPage.vue'
import Notification from '@/views/Dashboard/NotificationPage.vue'

// Auth
import LoginPage from '@/views/public/LoginPage.vue'
import LogoutPage from '@/views/Dashboard/LogoutPage.vue'

// Web
import Index from '@/views/public/Layout/WebLayout.vue'
import Home from '@/views/public/HomePage.vue'

const dashboard = {
  path: '/admin',
  redirect: '/admin/dashboard',
  component: DashboardLayout,
  children: [
    {
      path: 'dashboard',
      name: 'Dashboard',
      components: { default: Dashboard },
      meta: { requiresAuth: true }
    },
    {
      path: 'table',
      name: 'Table',
      component: Table,
      meta: { requiresAuth: true }
    },
    {
      path: 'notifications',
      name: 'Notifications',
      component: Notification,
      meta: { requiresAuth: true }
    },
    {
      path: 'icons',
      name: 'Icons',
      component: Icon,
      meta: { requiresAuth: true }
    },
    {
      path: 'settings',
      name: 'Settings',
      component: Dashboard,
      meta: { requiresAuth: true }
    },
    {
      path: 'logout',
      name: 'Logout',
      component: LogoutPage,
      meta: { requiresAuth: true }
    }
  ]
}

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/home',
    component: Index,
    children: [
      {
        path: 'home',
        name: 'Home',
        components: { default: Home },
        meta: { requiresAuth: false }
      },
      {
        path: 'login',
        name: 'Login',
        component: LoginPage,
        meta: { requiresAuth: false }
      }
    ]
  },
  dashboard,
  {
    path: '/:pathMatch(.*)*',
    redirect: '/home'
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior() {
    // always scroll to top
    return { top: 0 }
  }
})

router.beforeEach((to, from, next) => {
  const { authenticating, user } = useAuth()

  // Not logged into a guarded route?
  if (authenticating.value === false && to.meta.requiresAuth === true && !user?.value) {
    next({ name: 'Login' })
  } else next()
})

export default router
