import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import { useAuth } from '@/services/auth'

// Dashboard pages
import DashboardLayout from '@/views/Dashboard/Layout/DashboardLayout.vue'
import Dashboard from '@/views/Dashboard/DashboardMain.vue'

// Login
import LoginPage from '@/views/public/LoginPage.vue'

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
      path: 'settings',
      name: 'Settings',
      component: Dashboard,
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
  scrollBehavior(to, from, savedPosition) {
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
