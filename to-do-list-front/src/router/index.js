import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../components/Home.vue';
import Tasks from '../components/Tasks.vue';
import Login from '../components/Login.vue';
import Signup from '../components/Signup.vue';
import store from '@/store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    beforeEnter (to, from, next) {
      if (!store.getters.isAuthenticated) {
        next('/login')
      } else {
        next()
      }
    }
  },
  {
    path: '/tasks/:id',
    name: 'Tasks',
    component: Tasks,
    beforeEnter (to, from, next) {
      if (!store.getters.isAuthenticated) {
        next('/login')
      } else {
        next()
      }
    }
  }, 
  {
    path: '/login',
    name: 'Login',
    component: Login
  }, 
  {
    path: '/signup',
    name: 'Signup',
    component: Signup
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
