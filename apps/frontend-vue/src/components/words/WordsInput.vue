<template>
  <div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-2">単語リスト入力</h2>
      <p class="text-gray-600">学習した単語や表現を入力してください。各行に1つずつ記入してください。</p>
    </div>

    <!-- 単語入力フォーム -->
    <div class="mb-6">
      <label for="words-input" class="block text-sm font-medium text-gray-700 mb-2">
        単語リスト (改行区切り)
      </label>
      <textarea
        id="words-input"
        v-model="wordsInput"
        class="w-full h-40 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-vertical"
        placeholder="例:&#10;銀行&#10;会社&#10;学校&#10;..."
        @input="updateWordsList"
      ></textarea>
      <div class="mt-2 text-sm text-gray-500">
        入力された単語数: {{ wordsList.length }}
      </div>
    </div>

    <!-- 単語プレビュー -->
    <div v-if="wordsList.length > 0" class="mb-6">
      <h3 class="text-lg font-semibold text-gray-700 mb-3">単語プレビュー</h3>
      <div class="flex flex-wrap gap-2">
        <span
          v-for="(word, index) in wordsList"
          :key="index"
          class="inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
        >
          {{ word }}
        </span>
      </div>
    </div>

    <!-- アクションボタン -->
    <div class="flex flex-col sm:flex-row gap-4">
      <button
        @click="generatePDF"
        :disabled="!canGeneratePDF"
        class="flex-1 bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
      >
        <span v-if="isGenerating" class="flex items-center justify-center">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 714 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          PDF生成中...
        </span>
        <span v-else>PDF生成</span>
      </button>
      

      
      <button
        @click="clearInput"
        class="flex-1 bg-gray-500 text-white py-3 px-6 rounded-md hover:bg-gray-600 transition-colors font-medium"
      >
        クリア
      </button>
    </div>

    <!-- エラーメッセージ -->
    <div v-if="errorMessage" class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-md">
      {{ errorMessage }}
    </div>

    <!-- 成功メッセージ -->
    <div v-if="successMessage" class="mt-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded-md">
      {{ successMessage }}
    </div>

    <!-- PDF プレビュー/ダウンロードセクション -->
    <div v-if="generatedPDF" class="mt-8 p-6 bg-gray-50 rounded-lg">
      <h3 class="text-lg font-semibold text-gray-800 mb-4">PDF生成完了</h3>
      
      <div class="flex flex-col sm:flex-row gap-4 mb-4">
        <div class="flex-1">
          <p class="text-sm text-gray-600">
            ファイル名: {{ generatedPDF.filename }}<br>
            サイズ: {{ formatFileSize(generatedPDF.size) }}<br>
            単語数: {{ generatedPDF.word_count }}個
          </p>
        </div>
      </div>

      <div class="flex flex-col sm:flex-row gap-4">
        <button
          @click="downloadPDF"
          class="flex-1 bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors"
        >
          📁 PDFダウンロード
        </button>
        
        <button
          @click="previewPDF"
          class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
        >
          👁️ プレビュー
        </button>
      </div>
    </div>

    <!-- PDF プレビューモーダル -->
    <div v-if="showPreview" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="closePreview">
      <div class="bg-white p-4 rounded-lg max-w-5xl max-h-[90vh] w-full m-4" @click.stop>
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold">PDFプレビュー</h3>
          <button @click="closePreview" class="text-gray-500 hover:text-gray-700">
            ✕
          </button>
        </div>
        <iframe
          :src="pdfPreviewUrl"
          class="w-full h-96 border border-gray-300"
          title="PDF Preview"
        ></iframe>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { pdfApi } from '@/services/pdf'

export default {
  name: 'WordsInput',
  setup() {
    const wordsInput = ref('')
    const wordsList = ref([])
    const isGenerating = ref(false)
    const errorMessage = ref('')
    const successMessage = ref('')
    const generatedPDF = ref(null)
    const showPreview = ref(false)
    const pdfPreviewUrl = ref('')

    const canGeneratePDF = computed(() => {
      return wordsList.value.length > 0 && !isGenerating.value
    })

    const updateWordsList = () => {
      const words = wordsInput.value
        .split('\n')
        .map(word => word.trim())
        .filter(word => word.length > 0)
      wordsList.value = words
    }

    const clearInput = () => {
      wordsInput.value = ''
      wordsList.value = []
      errorMessage.value = ''
      successMessage.value = ''
      generatedPDF.value = null
    }

    const generateTestPDF = async () => {
      if (!canGeneratePDF.value) return

      isGenerating.value = true
      errorMessage.value = ''
      successMessage.value = ''

      try {
        console.log('Generating test PDF with words:', wordsList.value)
        const response = await pdfApi.generateTestPDF(wordsList.value)
        
        if (response.success) {
          generatedPDF.value = response
          successMessage.value = `テストPDF生成が完了しました！${response.word_count}個の単語を処理しました。`
        } else {
          errorMessage.value = response.error || 'テストPDF生成に失敗しました'
        }
      } catch (error) {
        console.error('Test PDF generation error:', error)
        console.error('Error response:', error.response?.data)
        
        let errorMsg = 'テストPDF生成中にエラーが発生しました。'
        
        if (error.response) {
          const status = error.response.status
          const data = error.response.data
          errorMsg = `エラー (${status}): ${data?.detail || error.message}`
        } else if (error.request) {
          errorMsg = 'サーバーに接続できません。'
        } else {
          errorMsg = `予期しないエラー: ${error.message}`
        }
        
        errorMessage.value = errorMsg
      } finally {
        isGenerating.value = false
      }
    }

    const generatePDF = async () => {
      if (!canGeneratePDF.value) return

      isGenerating.value = true
      errorMessage.value = ''
      successMessage.value = ''

      try {
        // まずPDFサービスのヘルスチェックを実行
        console.log('PDF health check...')
        await pdfApi.healthCheck()
        console.log('PDF service is healthy')
        
        console.log('Generating PDF with words:', wordsList.value)
        const response = await pdfApi.generateFromWords(wordsList.value)
        
        if (response.success) {
          generatedPDF.value = response
          successMessage.value = `PDF生成が完了しました！${response.word_count}個の単語を処理しました。`
        } else {
          errorMessage.value = response.error || 'PDF生成に失敗しました'
        }
      } catch (error) {
        console.error('PDF generation error:', error)
        console.error('Error response:', error.response?.data)
        
        let errorMsg = 'PDF生成中にエラーが発生しました。'
        
        if (error.response) {
          // サーバーエラーレスポンス
          const status = error.response.status
          const data = error.response.data
          
          if (status === 401) {
            errorMsg = 'ログインが必要です。再度ログインしてください。'
          } else if (status === 403) {
            errorMsg = 'アクセス権限がありません。'
          } else if (status === 404) {
            errorMsg = 'PDF生成APIが見つかりません。サーバー設定を確認してください。'
          } else if (status === 500) {
            errorMsg = `サーバーエラーが発生しました: ${data?.detail || '内部エラー'}`
          } else {
            errorMsg = `エラー (${status}): ${data?.detail || error.message}`
          }
        } else if (error.request) {
          // リクエストが送信されたが、レスポンスがない
          errorMsg = 'サーバーに接続できません。サーバーが起動しているか確認してください。'
        } else {
          // その他のエラー
          errorMsg = `予期しないエラー: ${error.message}`
        }
        
        errorMessage.value = errorMsg
      } finally {
        isGenerating.value = false
      }
    }

    const downloadPDF = () => {
      if (!generatedPDF.value) return

      const blob = new Blob(
        [Uint8Array.from(atob(generatedPDF.value.pdf_base64), c => c.charCodeAt(0))],
        { type: 'application/pdf' }
      )
      
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = generatedPDF.value.filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    }

    const previewPDF = () => {
      if (!generatedPDF.value) return

      const blob = new Blob(
        [Uint8Array.from(atob(generatedPDF.value.pdf_base64), c => c.charCodeAt(0))],
        { type: 'application/pdf' }
      )
      
      pdfPreviewUrl.value = URL.createObjectURL(blob)
      showPreview.value = true
    }

    const closePreview = () => {
      showPreview.value = false
      if (pdfPreviewUrl.value) {
        URL.revokeObjectURL(pdfPreviewUrl.value)
        pdfPreviewUrl.value = ''
      }
    }

    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    return {
      wordsInput,
      wordsList,
      isGenerating,
      errorMessage,
      successMessage,
      generatedPDF,
      showPreview,
      pdfPreviewUrl,
      canGeneratePDF,
      updateWordsList,
      clearInput,
      generatePDF,
      generateTestPDF,
      downloadPDF,
      previewPDF,
      closePreview,
      formatFileSize
    }
  }
}
</script>