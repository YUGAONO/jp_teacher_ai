import { createRouter, createWebHistory } from 'vue-router'
import WordsInput from '@/components/words/WordsInput.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: '/words'
    },
    {
      path: '/words',
      name: 'words',
      component: WordsInput,
      meta: {
        title: '単語学習PDF生成'
      }
    }
  ],
})

// タイトル設定
router.beforeEach((to, from, next) => {
  document.title = to.meta?.title as string || 'JP Teacher AI'
  next()
})

export default router
