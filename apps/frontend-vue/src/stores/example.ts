import { ref } from 'vue'
import { defineStore } from 'pinia'
import { exampleService } from '@/services'
import type { ExampleRequest } from '@/types'

export const useExampleStore = defineStore('example', () => {
  const examples = ref<string[]>([])
  const isLoading = ref(false)
  const currentWord = ref('')
  const currentLevel = ref('5')

  const generateExamples = async (request: ExampleRequest) => {
    try {
      isLoading.value = true
      currentWord.value = request.word
      currentLevel.value = request.level

      const response = await exampleService.generateExamples(request)
      examples.value = response.examples

      return { success: true, data: response.examples }
    } catch (error: any) {
      return { 
        success: false, 
        message: error.response?.data?.detail || '例文生成に失敗しました' 
      }
    } finally {
      isLoading.value = false
    }
  }

  const clearExamples = () => {
    examples.value = []
    currentWord.value = ''
    currentLevel.value = '5'
  }

  return {
    examples,
    isLoading,
    currentWord,
    currentLevel,
    generateExamples,
    clearExamples
  }
})