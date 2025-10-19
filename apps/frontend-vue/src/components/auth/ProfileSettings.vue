<template>
  <div class="profile-settings">
    <h4 class="text-white font-semibold mb-4">プロフィール設定</h4>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label class="block text-white text-sm font-medium mb-1">
          表示名
        </label>
        <input
          v-model="form.displayName"
          type="text"
          class="w-full px-3 py-2 bg-white bg-opacity-20 text-white placeholder-gray-300 border border-white border-opacity-30 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
          placeholder="表示名"
        />
      </div>
      
      <div>
        <label class="block text-white text-sm font-medium mb-1">
          言語
        </label>
        <select
          v-model="form.locale"
          class="w-full px-3 py-2 bg-white bg-opacity-20 text-white border border-white border-opacity-30 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
        >
          <option value="ja" class="text-gray-800">日本語</option>
          <option value="en" class="text-gray-800">English</option>
        </select>
      </div>
      
      <div>
        <label class="block text-white text-sm font-medium mb-1">
          プラン
        </label>
        <select
          v-model="form.currentPlan"
          class="w-full px-3 py-2 bg-white bg-opacity-20 text-white border border-white border-opacity-30 rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
        >
          <option value="free" class="text-gray-800">Free</option>
          <option value="premium" class="text-gray-800">Premium</option>
          <option value="enterprise" class="text-gray-800">Enterprise</option>
        </select>
      </div>
      
      <button
        type="submit"
        :disabled="isLoading || !hasChanges"
        class="w-full bg-white bg-opacity-20 text-white py-2 px-4 rounded-md hover:bg-opacity-30 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <span v-if="isLoading">更新中...</span>
        <span v-else>プロフィール更新</span>
      </button>
    </form>
    
    <div v-if="message" class="mt-4">
      <div
        :class="{
          'text-green-200': isSuccess,
          'text-red-200': !isSuccess
        }"
        class="text-sm"
      >
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/counter'

const authStore = useAuthStore()
const { user, isLoading } = storeToRefs(authStore)

const form = reactive({
  displayName: '',
  locale: 'ja',
  currentPlan: 'free'
})

const message = ref('')
const isSuccess = ref(false)

// Initialize form with user data
watch(user, (newUser) => {
  if (newUser) {
    form.displayName = newUser.display_name || ''
    form.locale = newUser.locale || 'ja'
    form.currentPlan = newUser.current_plan || 'free'
  }
}, { immediate: true })

const hasChanges = computed(() => {
  if (!user.value) return false
  
  return form.displayName !== user.value.display_name ||
         form.locale !== user.value.locale ||
         form.currentPlan !== user.value.current_plan
})

const handleSubmit = async () => {
  if (!hasChanges.value) {
    message.value = '変更がありませんでした'
    isSuccess.value = false
    return
  }

  message.value = ''
  
  const updates: any = {}
  
  if (form.displayName !== user.value?.display_name) {
    updates.display_name = form.displayName
  }
  if (form.locale !== user.value?.locale) {
    updates.locale = form.locale
  }
  if (form.currentPlan !== user.value?.current_plan) {
    updates.current_plan = form.currentPlan
  }

  const result = await authStore.updateProfile(updates)
  
  message.value = result.message
  isSuccess.value = result.success
}
</script>

<style scoped>
.profile-settings {
  padding: 0;
}
</style>