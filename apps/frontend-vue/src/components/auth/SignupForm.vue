<template>
  <div class="auth-form">
    <h3 class="text-lg font-semibold mb-4">新規登録</h3>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label for="signup-email" class="block text-sm font-medium text-gray-700 mb-1">
          メールアドレス
        </label>
        <input
          id="signup-email"
          v-model="form.email"
          type="email"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="メールアドレスを入力"
        />
      </div>
      
      <div>
        <label for="signup-password" class="block text-sm font-medium text-gray-700 mb-1">
          パスワード
        </label>
        <input
          id="signup-password"
          v-model="form.password"
          type="password"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="パスワードを入力"
        />
      </div>
      
      <div>
        <label for="confirm-password" class="block text-sm font-medium text-gray-700 mb-1">
          パスワード確認
        </label>
        <input
          id="confirm-password"
          v-model="form.confirmPassword"
          type="password"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="パスワードを再入力"
        />
      </div>
      
      <div>
        <label for="display-name" class="block text-sm font-medium text-gray-700 mb-1">
          表示名
        </label>
        <input
          id="display-name"
          v-model="form.displayName"
          type="text"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="表示名を入力"
        />
      </div>
      
      <div>
        <label for="locale" class="block text-sm font-medium text-gray-700 mb-1">
          言語
        </label>
        <select
          id="locale"
          v-model="form.locale"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="ja">日本語</option>
          <option value="en">English</option>
        </select>
      </div>
      
      <button
        type="submit"
        :disabled="isLoading || !isFormValid"
        class="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="isLoading">登録中...</span>
        <span v-else>新規登録</span>
      </button>
    </form>
    
    <div v-if="message" class="mt-4">
      <div
        :class="{
          'text-green-600': isSuccess,
          'text-red-600': !isSuccess
        }"
        class="text-sm"
      >
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useAuthStore } from '@/stores/counter'

const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  displayName: '',
  locale: 'ja'
})

const message = ref('')
const isSuccess = ref(false)
const isLoading = ref(false)

const isFormValid = computed(() => {
  return form.email && 
         form.password && 
         form.confirmPassword && 
         form.displayName &&
         form.password === form.confirmPassword
})

const handleSubmit = async () => {
  if (!isFormValid.value) {
    message.value = '全ての項目を正しく入力してください'
    isSuccess.value = false
    return
  }

  if (form.password !== form.confirmPassword) {
    message.value = 'パスワードが一致しません'
    isSuccess.value = false
    return
  }

  isLoading.value = true
  message.value = ''

  const result = await authStore.signup({
    email: form.email,
    password: form.password,
    display_name: form.displayName,
    locale: form.locale
  })

  message.value = result.message
  isSuccess.value = result.success
  isLoading.value = false

  if (result.success) {
    // Reset form
    Object.assign(form, {
      email: '',
      password: '',
      confirmPassword: '',
      displayName: '',
      locale: 'ja'
    })
  }
}
</script>

<style scoped>
.auth-form {
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  background-color: white;
}
</style>