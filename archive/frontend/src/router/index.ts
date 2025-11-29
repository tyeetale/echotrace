import { createRouter, createWebHistory } from 'vue-router'
import ConversationPage from '../pages/ConversationPage.vue'

const routes = [
  {
    path: '/',
    name: 'conversations',
    component: ConversationPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router