<template>
  <div class="example-form">
    <!-- <h2 class="text-2xl font-bold mb-6">例文生成</h2> -->
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div class="form-row">
        <div class="form-group">
          <label for="word" class="block text-sm font-medium text-gray-700 mb-1">
            単語を入力してください
          </label>
          <input
            id="word"
            v-model="form.word"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="例: 勉強"
          />
        </div>
        
        <div class="form-group">
          <label for="level" class="block text-sm font-medium text-gray-700 mb-1">
            JLPTレベル
          </label>
          <select
            id="level"
            v-model="form.level"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="5">N5</option>
            <option value="4">N4</option>
            <option value="3">N3</option>
            <option value="2">N2</option>
            <option value="1">N1</option>
          </select>
        </div>
        
        <div class="form-group">
          <button
            type="submit"
            :disabled="isLoading || !form.word.trim()"
            class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading">生成中...</span>
            <span v-else>例文を生成</span>
          </button>
        </div>
      </div>
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
import { useExampleStore } from '@/stores/example'

const exampleStore = useExampleStore()

const form = reactive({
  word: '勉強',
  level: '5'
})

const message = ref('')
const isSuccess = ref(false)
const isLoading = ref(false)

const handleSubmit = async () => {
  if (!form.word.trim()) {
    message.value = '単語を入力してください'
    isSuccess.value = false
    return
  }

  isLoading.value = true
  message.value = ''

  const result = await exampleStore.generateExamples({
    word: form.word.trim(),
    level: form.level
  })

  if (result.success) {
    message.value = `「${form.word}」のJLPT N${form.level}レベルの例文を生成しました！`
    isSuccess.value = true
  } else {
    message.value = result.message || '例文生成に失敗しました'
    isSuccess.value = false
  }

  isLoading.value = false
}
</script>

<style scoped>
.example-form {
  padding: 1.5rem;
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 1rem;
  align-items: end;
}

.form-group {
  display: flex;
  flex-direction: column;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>