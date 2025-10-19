<template>
  <div class="auth-form">
    <h3 class="text-lg font-semibold mb-4">ログイン</h3>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
          メールアドレス
        </label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="メールアドレスを入力"
        />
      </div>
      
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
          パスワード
        </label>
        <input
          id="password"
          v-model="form.password"
          type="password"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="パスワードを入力"
        />
      </div>
      
      <button
        type="submit"
        :disabled="isLoading || !form.email || !form.password"
        class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="isLoading">ログイン中...</span>
        <span v-else>ログイン</span>
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
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/counter'

const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: ''
})

const message = ref('')
const isSuccess = ref(false)
const isLoading = ref(false)

const handleSubmit = async () => {
  if (!form.email || !form.password) {
    message.value = 'メールアドレスとパスワードを入力してください'
    isSuccess.value = false
    return
  }

  isLoading.value = true
  message.value = ''

  const result = await authStore.login({
    email: form.email,
    password: form.password
  })

  message.value = result.message
  isSuccess.value = result.success
  isLoading.value = false

  if (result.success) {
    // Reset form
    form.email = ''
    form.password = ''
  }
}
</script>

<style scoped>
.auth-form {
  @apply p-4 border border-gray-200 rounded-lg bg-white;
}
</style>