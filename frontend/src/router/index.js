// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/encode',
      name: 'encode',
      component: () => import('../views/EncodeView.vue')
    },
    {
      path: '/decode',
      name: 'decode',
      component: () => import('../views/DecodeView.vue')
    }
  ]
})

export default router