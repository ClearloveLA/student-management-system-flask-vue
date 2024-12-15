import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/auth/Login.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('../views/auth/Register.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      name: 'StudentList',
      component: () => import('../views/StudentList.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/statistics',
      name: 'Statistics',
      component: () => import('../views/Statistics.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/settings',
      name: 'Settings',
      component: () => import('../views/Settings.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('../views/Profile.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/logs',
      name: 'OperationLogs',
      component: () => import('../views/OperationLogs.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)

  if (requiresAuth && !token) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && token) {
    // 如果已登录，访问登录页则重定向到首页
    next('/')
  } else {
    next()
  }
})

export default router 