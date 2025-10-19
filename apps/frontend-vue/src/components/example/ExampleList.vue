<template>
  <div v-if="examples.length > 0" class="example-list">
    <div class="mb-4">
      <!-- <h3 class="text-xl font-semibold">生成された例文:</h3> -->
      <p class="text-gray-600">「{{ currentWord }}」(JLPT N{{ currentLevel }})</p>
    </div>
    
    <div class="examples-grid">
      <div
        v-for="(example, index) in examples"
        :key="index"
        class="example-card"
      >
        <div class="example-number">{{ index + 1 }}</div>
        <div class="example-text">{{ example }}</div>
      </div>
    </div>
  </div>
  
  <div v-else-if="!isLoading" class="no-examples">
    <p class="text-gray-500 text-center">
      単語とJLPTレベルを入力して、例文を生成してください。
    </p>
  </div>
  
  <div v-if="isLoading" class="loading">
    <div class="loading-spinner"></div>
    <p class="text-center text-gray-600">例文を生成中...</p>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useExampleStore } from '@/stores/example'

const exampleStore = useExampleStore()
const { examples, isLoading, currentWord, currentLevel } = storeToRefs(exampleStore)
</script>

<style scoped>
.example-list {
  margin-top: 2rem;
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 0.5rem;
}

.examples-grid {
  display: grid;
  gap: 1rem;
}

.example-card {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  background-color: white;
  border-radius: 0.375rem;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.example-number {
  flex-shrink: 0;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #3b82f6;
  color: white;
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: 600;
}

.example-text {
  flex: 1;
  line-height: 1.6;
  color: #374151;
}

.no-examples {
  margin-top: 2rem;
  padding: 3rem 1rem;
  text-align: center;
  background-color: #f9fafb;
  border-radius: 0.5rem;
  border: 2px dashed #d1d5db;
}

.loading {
  margin-top: 2rem;
  padding: 2rem;
  text-align: center;
}

.loading-spinner {
  width: 2rem;
  height: 2rem;
  margin: 0 auto 1rem;
  border: 2px solid #e5e7eb;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>