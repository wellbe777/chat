import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import Login from './pages/Login.vue'
import Register from './pages/Register.vue'
import NotFound from './pages/NotFound.vue'
import Chat from './pages/Chat.vue'
import { useCookies } from 'vue3-cookies'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '',
      component: Home
    },
    {
      path: '/login',
      component: Login
    },
    {
      path: '/register',
      component: Register
    },
    {
      path: '/chat',
      component: Chat,
      meta: {
        auth: true
      }
    },
    { path: "/:pathMatch(.*)*", component: NotFound }
  ]
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((route) => route.meta && route.meta.auth)
  const { cookies } = useCookies()
  const token = cookies.get('jwt')
  if (requiresAuth && !token) {
    next({path: "/login"})
  } else if (token && (to.fullPath === "/login" || to.fullPath === "/register")) {
    next({path: "/"})
  } else {
    next()
  }
})

export default router