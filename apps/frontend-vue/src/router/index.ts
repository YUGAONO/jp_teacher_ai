import { createRouter, createWebHistory } from 'vue-router'
import WordsInput from '@/components/words/WordsInput.vue'
import ExampleForm from '@/components/example/ExampleForm.vue'
import ExampleList from '@/components/example/ExampleList.vue'

// 例文生成画面用のラッパーコンポーネント
const ExamplesView = {
  template: `
    <div>
      <ExampleForm />
      <ExampleList />
    </div>
  `,
  components: {
    ExampleForm,
    ExampleList
  }
}

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
    },
    {
      path: '/examples',
      name: 'examples',
      component: ExamplesView,
      meta: {
        title: '例文生成'
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
